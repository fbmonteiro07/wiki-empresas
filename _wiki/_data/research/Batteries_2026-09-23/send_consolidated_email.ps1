param(
    [switch]$Send,
    [switch]$Verify
)
$ErrorActionPreference = 'Stop'
$recipientAddress = 'felipe.monteiro@capstone.com.br'
$exportsDirectory = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot 'exports')) + [IO.Path]::DirectorySeparatorChar
$manifestPath = Join-Path $exportsDirectory 'email_manifest.json'
$manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($manifest.recipient -ine $recipientAddress) { throw 'Unexpected recipient in manifest.' }
$subject = [string]$manifest.subject
$bodyFile = (Get-Item -LiteralPath $manifest.body_path).FullName
$attachmentFile = (Get-Item -LiteralPath $manifest.attachment_path).FullName
foreach ($path in @($bodyFile, $attachmentFile)) {
    if (!$path.StartsWith($exportsDirectory, [StringComparison]::OrdinalIgnoreCase) -or [IO.Path]::GetExtension($path) -ine '.html') { throw 'Only the generated HTML report in this research export directory is allowed.' }
    if ((Get-Item -LiteralPath $path).Length -gt 3MB) { throw 'Report exceeds 3 MB.' }
}
$bodyHtml = Get-Content -LiteralPath $bodyFile -Raw -Encoding UTF8
if ([string]::IsNullOrWhiteSpace($bodyHtml) -or [string]::IsNullOrWhiteSpace($subject)) { throw 'Empty body or subject.' }
$outlookApp = New-Object -ComObject Outlook.Application
$account = @($outlookApp.Session.Accounts | Where-Object { $_.SmtpAddress -ieq $recipientAddress })
if ($account.Count -ne 1) { throw 'Expected Outlook account unavailable or ambiguous.' }
$sentFolder = $account[0].DeliveryStore.GetDefaultFolder(5)
$outboxFolder = $account[0].DeliveryStore.GetDefaultFolder(4)
$filter = "[Subject] = '" + $subject.Replace("'", "''") + "'"
$receiptPath = Join-Path $exportsDirectory 'email_send_receipt.json'

function Get-RecipientSmtp($recipient) {
    if ($recipient.AddressEntry.Type -eq 'EX') { return $recipient.AddressEntry.GetExchangeUser().PrimarySmtpAddress }
    return $recipient.Address
}

function Save-Receipt([string]$state, [string]$entryId = '') {
    $receipt = [ordered]@{
        status=$state
        subject=$subject
        recipient=$recipientAddress
        attachment=$attachmentFile
        attachment_sha256=(Get-FileHash -LiteralPath $attachmentFile -Algorithm SHA256).Hash
        body_sha256=(Get-FileHash -LiteralPath $bodyFile -Algorithm SHA256).Hash
        recorded_at=[DateTime]::UtcNow.ToString('o')
        entry_id=$entryId
    }
    $receipt | ConvertTo-Json | Set-Content -LiteralPath $receiptPath -Encoding UTF8
    $receipt | ConvertTo-Json -Compress
}

function Find-Sent {
    $matches = $sentFolder.Items.Restrict($filter)
    if ($matches.Count -eq 0) { return $null }
    if ($matches.Count -gt 1) { throw 'More than one matching sent message. Inspect; do not resend.' }
    $mail = $matches.Item(1)
    if (!$mail.Sent -or $mail.Recipients.Count -ne 1) { throw 'Matching message has unexpected recipient count or sent state.' }
    if ((Get-RecipientSmtp $mail.Recipients.Item(1)) -ine $recipientAddress) { throw 'Matching message has an unexpected recipient.' }
    $attachmentNames = @($mail.Attachments | ForEach-Object { $_.FileName })
    if ($attachmentNames.Count -ne 1 -or $attachmentNames[0] -ne [IO.Path]::GetFileName($attachmentFile)) { throw 'Matching sent message has unexpected attachments.' }
    if (!$mail.HTMLBody.Contains('39.3%') -or !$mail.HTMLBody.Contains('15.5%') -or !$mail.HTMLBody.Contains('Coatue')) { throw 'Matching sent message has an unexpected body.' }
    return $mail
}

$existing = Find-Sent
if ($null -ne $existing) { Save-Receipt 'sent_confirmed' $existing.EntryID; exit 0 }
if ($outboxFolder.Items.Restrict($filter).Count -gt 0) { Save-Receipt 'pending_outbox'; exit 2 }
if ($Verify) {
    if (Test-Path -LiteralPath $receiptPath) { Get-Content -LiteralPath $receiptPath -Raw }
    else { Write-Output '{"status":"not_sent"}' }
    exit 2
}
if (Test-Path -LiteralPath $receiptPath) { throw 'Prior attempt exists. Verify its state before any retry.' }
if (!$Send) {
    [ordered]@{status='validated_not_sent';recipient=$recipientAddress;subject=$subject;attachment=$attachmentFile;bytes=(Get-Item -LiteralPath $attachmentFile).Length} | ConvertTo-Json -Compress
    exit 0
}
$mail = $outlookApp.CreateItem(0)
$mail.SendUsingAccount = $account[0]
$mail.SaveSentMessageFolder = $sentFolder
$mail.DeleteAfterSubmit = $false
$mail.Subject = $subject
$mail.BodyFormat = 2
$mail.HTMLBody = $bodyHtml
$null = $mail.Recipients.Add($recipientAddress)
if (!$mail.Recipients.ResolveAll() -or $mail.Recipients.Count -ne 1) { throw 'Could not resolve the sole recipient.' }
if ((Get-RecipientSmtp $mail.Recipients.Item(1)) -ine $recipientAddress) { throw 'Resolved recipient differs from the authorized self address.' }
$null = $mail.Attachments.Add($attachmentFile)
$mail.Save()
Save-Receipt 'pending_dispatch' $mail.EntryID
# Record intent before dispatch to prevent a duplicate send after an ambiguous response.
$mail.Send()
for ($attempt = 0; $attempt -lt 20; $attempt++) {
    Start-Sleep -Seconds 1
    $confirmed = Find-Sent
    if ($null -ne $confirmed) { Save-Receipt 'sent_confirmed' $confirmed.EntryID; exit 0 }
}
if ($outboxFolder.Items.Restrict($filter).Count -gt 0) { Save-Receipt 'pending_outbox'; exit 2 }
Save-Receipt 'submitted_unconfirmed'
exit 2
