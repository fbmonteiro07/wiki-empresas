<#
credit_mail_collect.ps1 - mail window for the AI credit alerts (credit_alerts.py --mail).
Outlook desktop over COM: every mail folder of the Felipe account except Sent/Outbox/Drafts/Deleted/Junk,
store-side DASL window on ReceivedTime, subject + sender + body (capped) for every arrival. The credit / name
matching happens in Python (patterns live in _data/credit_watch_config.json -> mail), so this file stays dumb.
Writes <OutputDirectory>\mail.json (array of {id, subject, sender, sender_name, date, folder, body}) and
mail-coverage.json (window, counts, newest_received_utc, inbox_lag_hours - a large lag means Outlook desktop
is not syncing and the task should fall back to the M365 connector). ASCII only; PowerShell 5.1.
Usage: powershell -NoProfile -ExecutionPolicy Bypass -File credit_mail_collect.ps1 -SinceUtc 2026-10-13T12:00:00Z -OutputDirectory <dir> [-MaxItems 1500] [-BodyChars 15000]
#>
param(
 [Parameter(Mandatory=$true)][string]$SinceUtc,
 [Parameter(Mandatory=$true)][string]$OutputDirectory,
 [int]$MaxItems = 1500,
 [int]$BodyChars = 15000
)
$ErrorActionPreference = 'Stop'
$since = [DateTimeOffset]::Parse($SinceUtc).UtcDateTime
$until = [DateTime]::UtcNow
[void][IO.Directory]::CreateDirectory($OutputDirectory)
$app = New-Object -ComObject Outlook.Application
$ns = $app.GetNamespace('MAPI')
$account = @($ns.Accounts | Where-Object { $_.SmtpAddress -ieq 'felipe.monteiro@capstone.com.br' })
if ($account.Count -ne 1) { throw 'Account felipe.monteiro@capstone.com.br unavailable or ambiguous in Outlook' }
$store = $account[0].DeliveryStore
$folders = [Collections.Generic.List[object]]::new()
function Walk-Mail($folder, $depth) {
 if ($depth -gt 5) { return }
 if ($folder.Name -match '^(Sent Items|Outbox|Drafts|Itens Enviados|Caixa de Sa.da|Rascunhos|Deleted Items|Itens Exclu.dos|Junk E.?mail|Lixo Eletr.nico|Sync Issues|Problemas de Sincroniza..o|Conversation History|Hist.rico de Conversas)$') { return }
 if ($folder.DefaultItemType -eq 0) { $folders.Add($folder) }
 foreach ($child in $folder.Folders) { Walk-Mail $child ($depth + 1) }
}
Walk-Mail ($store.GetRootFolder()) 0
$inbox = $ns.GetDefaultFolder(6)
$newest = $null
try {
 $probe = $inbox.Items; $probe.Sort('[ReceivedTime]', $true)
 $first = $probe.GetFirst(); if ($null -ne $first) { $newest = $first.ReceivedTime.ToUniversalTime() }
} catch {}
$cut = '@SQL="urn:schemas:httpmail:datereceived" >= ''' + $since.ToLocalTime().ToString('yyyy-MM-dd HH:mm') + ''''
$rows = [Collections.Generic.List[object]]::new()
$seen = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
$audit = [Collections.Generic.List[object]]::new()
$screened = 0
foreach ($folder in $folders) {
 try { $items = $folder.Items.Restrict($cut); $count = $items.Count } catch { $audit.Add(@{folder=$folder.FolderPath; error=$_.Exception.Message}); continue }
 if ($count -eq 0) { continue }
 for ($i = 1; $i -le $count; $i++) {
  if ($rows.Count -ge $MaxItems) { break }
  $item = $items.Item($i)
  try {
   if ($item.Class -eq 43) {
    $id = [string]$item.EntryID
    if ($seen.Add($id)) {
     $screened++
     $sender = ([string]$item.SenderEmailAddress).ToLowerInvariant()
     if ($item.SenderEmailType -eq 'EX') { try { $sender = ([string]$item.Sender.GetExchangeUser().PrimarySmtpAddress).ToLowerInvariant() } catch {} }
     $body = ''
     try { $body = [string]$item.Body } catch {}
     if ($body.Length -gt $BodyChars) { $body = $body.Substring(0, $BodyChars) + ' [...]' }
     $rows.Add(@{id=$id; subject=[string]$item.Subject; sender=$sender; sender_name=[string]$item.SenderName;
                 date=$item.ReceivedTime.ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ'); folder=$folder.FolderPath; body=$body})
    }
   }
  } catch { $audit.Add(@{folder=$folder.FolderPath; error=$_.Exception.Message}) }
 }
}
$enc = New-Object System.Text.UTF8Encoding($false)
[IO.File]::WriteAllText((Join-Path $OutputDirectory 'mail.json'), (ConvertTo-Json -InputObject @($rows.ToArray()) -Depth 4), $enc)
$lag = $null
if ($null -ne $newest) { $lag = [Math]::Round(($until - $newest).TotalHours, 2) }
$coverage = @{since_utc=$since.ToString('yyyy-MM-ddTHH:mm:ssZ'); until_utc=$until.ToString('yyyy-MM-ddTHH:mm:ssZ'); screened=$screened; collected=$rows.Count;
              folders=$folders.Count; newest_received_utc=$(if ($null -ne $newest) { $newest.ToString('yyyy-MM-ddTHH:mm:ssZ') } else { $null });
              inbox_lag_hours=$lag; audit=@($audit.ToArray())}
[IO.File]::WriteAllText((Join-Path $OutputDirectory 'mail-coverage.json'), ($coverage | ConvertTo-Json -Depth 4), $enc)
Write-Output ("collected {0} of {1} screened mails since {2}; newest {3}; lag {4} h" -f $rows.Count, $screened, $since.ToString('u'), $coverage.newest_received_utc, $lag)
