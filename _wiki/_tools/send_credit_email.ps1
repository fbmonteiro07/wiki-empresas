param(
    [Parameter(Mandatory=$true)][string]$BodyPath,
    [Parameter(Mandatory=$true)][string]$AttachmentPath,
    [Parameter(Mandatory=$true)][string]$Subject,
    [switch]$Send,
    [switch]$Verify
)
$ErrorActionPreference = 'Stop'
$recipientAddress = 'felipe.monteiro@capstone.com.br'
$reportsDirectory = Join-Path (Split-Path -Parent $PSScriptRoot) '_data\credit-monitor'
$exportsDirectory = [IO.Path]::GetFullPath((Join-Path $reportsDirectory 'exports')) + [IO.Path]::DirectorySeparatorChar
$attachmentFile = (Get-Item -LiteralPath $AttachmentPath).FullName
if (!$attachmentFile.StartsWith($exportsDirectory, [StringComparison]::OrdinalIgnoreCase) -or [IO.Path]::GetExtension($attachmentFile) -ne '.html') {
    throw 'Attachment must be a generated HTML file in the credit-monitor exports directory.'
}
if ((Get-Item -LiteralPath $attachmentFile).Length -gt 3MB) { throw 'Attachment exceeds 3 MB.' }
$bodyText = Get-Content -LiteralPath $BodyPath -Raw -Encoding UTF8
if ([string]::IsNullOrWhiteSpace($bodyText) -or [string]::IsNullOrWhiteSpace($Subject)) { throw 'Empty email body or subject.' }
$outlookApp = New-Object -ComObject Outlook.Application
$account = @($outlookApp.Session.Accounts | Where-Object { $_.SmtpAddress -ieq $recipientAddress })
if ($account.Count -ne 1) { throw 'The expected Outlook sender account is unavailable or ambiguous.' }
$sentFolder = $account[0].DeliveryStore.GetDefaultFolder(5)
$outboxFolder = $account[0].DeliveryStore.GetDefaultFolder(4)
$filter = "[Subject] = '" + $Subject.Replace("'", "''") + "'"
$receiptDirectory = Join-Path $reportsDirectory 'email-receipts'
New-Item -ItemType Directory -Force -Path $receiptDirectory | Out-Null
$subjectBytes = [Text.Encoding]::UTF8.GetBytes($Subject)
$hasher = [Security.Cryptography.SHA256]::Create()
$subjectHash = [BitConverter]::ToString($hasher.ComputeHash($subjectBytes)).Replace('-','').ToLowerInvariant()
$receiptPath = Join-Path $receiptDirectory ($subjectHash + '.json')

function Save-Receipt([string]$State, [string]$EntryId = '') {
    $receipt = [ordered]@{status=$State; subject=$Subject; recipient=$recipientAddress; attachment=$attachmentFile; attachment_sha256=(Get-FileHash -LiteralPath $attachmentFile -Algorithm SHA256).Hash; recorded_at=[DateTime]::UtcNow.ToString('o'); entry_id=$EntryId}
    $receipt | ConvertTo-Json | Set-Content -LiteralPath $receiptPath -Encoding UTF8
    $receipt | ConvertTo-Json -Compress
}

function Find-Sent {
    $matches = $sentFolder.Items.Restrict($filter)
    if ($matches.Count -gt 0) {
        $mail = $matches.Item(1)
        $recipient = $mail.Recipients.Item(1)
        $smtpAddress = $recipient.Address
        if ($recipient.AddressEntry.Type -eq 'EX') { $smtpAddress = $recipient.AddressEntry.GetExchangeUser().PrimarySmtpAddress }
        $attachmentNames = @($mail.Attachments | ForEach-Object { $_.FileName })
        if (!$mail.Sent -or $mail.Recipients.Count -ne 1 -or $smtpAddress -ine $recipientAddress -or $attachmentNames -notcontains [IO.Path]::GetFileName($attachmentFile)) {
            throw 'Matching subject found, but recipient or attachment differs. Inspect Sent Items; do not resend.'
        }
        return $mail
    }
    return $null
}

$existing = Find-Sent
if ($null -ne $existing) { Save-Receipt 'sent_confirmed' $existing.EntryID; exit 0 }
if ($outboxFolder.Items.Restrict($filter).Count -gt 0) { Save-Receipt 'pending_outbox'; exit 2 }
if ($Verify) {
    if (Test-Path -LiteralPath $receiptPath) { Get-Content -LiteralPath $receiptPath -Raw }
    else { Write-Output '{"status":"not_sent"}' }
    exit 2
}
if (Test-Path -LiteralPath $receiptPath) { throw 'A prior attempt exists. Check the receipt and Sent Items before any retry.' }
if (!$Send) {
    [ordered]@{status='validated_not_sent';recipient=$recipientAddress;subject=$Subject;attachment=$attachmentFile;bytes=(Get-Item -LiteralPath $attachmentFile).Length} | ConvertTo-Json -Compress
    exit 0
}
$mail = $outlookApp.CreateItem(0)
$mail.SendUsingAccount = $account[0]
$mail.SaveSentMessageFolder = $sentFolder
$mail.DeleteAfterSubmit = $false
$mail.Subject = $Subject
$mail.Body = $bodyText
$null = $mail.Recipients.Add($recipientAddress)
if (!$mail.Recipients.ResolveAll() -or $mail.Recipients.Count -ne 1) { throw 'Could not resolve the sole recipient.' }
$null = $mail.Attachments.Add($attachmentFile)
$mail.Save()
Save-Receipt 'pending_dispatch' $mail.EntryID
# A pending receipt prevents blindly resending if Outlook's response is ambiguous.
$mail.Send()
for ($attempt = 0; $attempt -lt 15; $attempt++) {
    Start-Sleep -Seconds 1
    $confirmed = Find-Sent
    if ($null -ne $confirmed) { Save-Receipt 'sent_confirmed' $confirmed.EntryID; exit 0 }
}
Save-Receipt 'submitted_unconfirmed'
exit 2

