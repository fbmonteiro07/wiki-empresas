param([switch]$Send, [switch]$Verify)
$ErrorActionPreference = 'Stop'
$recipientAddress = 'fernanda.watkins@capstone.com.br'
$senderAddress = 'felipe.monteiro@capstone.com.br'
$bodyPath = Join-Path $PSScriptRoot 'email.html'
$subjectPath = Join-Path $PSScriptRoot 'email_subject.txt'
$receiptPath = Join-Path $PSScriptRoot 'email_receipt.json'
$bodyText = Get-Content -LiteralPath $bodyPath -Raw -Encoding UTF8
$subjectText = (Get-Content -LiteralPath $subjectPath -Raw -Encoding UTF8).Trim()
$bodyHash = (Get-FileHash -LiteralPath $bodyPath -Algorithm SHA256).Hash
$app = New-Object -ComObject Outlook.Application
$accounts = @($app.Session.Accounts | Where-Object { $_.SmtpAddress -ieq $senderAddress })
if ($accounts.Count -ne 1) { throw 'Expected Outlook sender is unavailable or ambiguous.' }
$account = $accounts[0]
$sentFolder = $account.DeliveryStore.GetDefaultFolder(5)
$outbox = $account.DeliveryStore.GetDefaultFolder(4)
$filter = "[Subject] = '" + $subjectText.Replace("'", "''") + "'"
function Save-Receipt([string]$status, [string]$entryId = '') {
    $receipt = [ordered]@{ status=$status; recipient=$recipientAddress; sender=$senderAddress; subject=$subjectText; body_sha256=$bodyHash; recorded_at=[DateTime]::UtcNow.ToString('o'); entry_id=$entryId }
    $receipt | ConvertTo-Json | Set-Content -LiteralPath $receiptPath -Encoding UTF8
    $receipt | ConvertTo-Json -Compress
}
function Find-Sent {
    $matches = $sentFolder.Items.Restrict($filter)
    if ($matches.Count -gt 1) { throw 'Multiple matching sent messages; inspect before retrying.' }
    if ($matches.Count -eq 0) { return $null }
    $mail = $matches.Item(1)
    if (!$mail.Sent -or $mail.Recipients.Count -ne 1) { throw 'Matching sent message has unexpected status or recipients.' }
    $recipient = $mail.Recipients.Item(1)
    $smtp = $recipient.Address
    if ($recipient.AddressEntry.Type -eq 'EX') { $smtp = $recipient.AddressEntry.GetExchangeUser().PrimarySmtpAddress }
    if ($smtp -ine $recipientAddress) { throw 'Matching subject has another recipient. Do not resend.' }
    if ($mail.HTMLBody -notmatch '111.5x' -or $mail.HTMLBody -notmatch '45.1x') { throw 'Matching message content differs. Do not resend.' }
    return $mail
}
$sent = Find-Sent
if ($null -ne $sent) { Save-Receipt 'sent_confirmed' $sent.EntryID; exit 0 }
if ($outbox.Items.Restrict($filter).Count -gt 0) { Save-Receipt 'pending_outbox'; exit 2 }
if ($Verify) {
    if (Test-Path -LiteralPath $receiptPath) { Get-Content -LiteralPath $receiptPath -Raw }
    else { Write-Output '{"status":"not_sent"}' }
    exit 2
}
if (Test-Path -LiteralPath $receiptPath) { throw 'Prior send attempt recorded. Verify before any retry.' }
if (!$Send) {
    [ordered]@{status='validated_not_sent';recipient=$recipientAddress;sender=$senderAddress;subject=$subjectText;body_sha256=$bodyHash} | ConvertTo-Json -Compress
    exit 0
}
$mail = $app.CreateItem(0)
$mail.SendUsingAccount = $account
$mail.SaveSentMessageFolder = $sentFolder
$mail.DeleteAfterSubmit = $false
$mail.Subject = $subjectText
$mail.HTMLBody = $bodyText
$null = $mail.Recipients.Add($recipientAddress)
if (!$mail.Recipients.ResolveAll() -or $mail.Recipients.Count -ne 1) { throw 'Could not resolve sole recipient.' }
$resolved = $mail.Recipients.Item(1)
$smtp = $resolved.Address
if ($resolved.AddressEntry.Type -eq 'EX') { $smtp = $resolved.AddressEntry.GetExchangeUser().PrimarySmtpAddress }
if ($smtp -ine $recipientAddress) { throw 'Resolved recipient differs from requested address.' }
$mail.Save()
Save-Receipt 'pending_dispatch' $mail.EntryID
$mail.Send()
for ($i=0; $i -lt 15; $i++) {
    Start-Sleep -Seconds 1
    $sent = Find-Sent
    if ($null -ne $sent) { Save-Receipt 'sent_confirmed' $sent.EntryID; exit 0 }
}
Save-Receipt 'submitted_unconfirmed'
exit 2
