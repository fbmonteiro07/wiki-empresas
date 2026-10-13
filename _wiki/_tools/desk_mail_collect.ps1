<#
desk_mail_collect.ps1 — mail screen for the 10:00 sentiment-radar desk review (Claude task).
Port (2026-10-13) of the retired Codex collect_daily_radar_mail.ps1: Outlook desktop over COM, store-side
DASL window on every mail folder (no Sent/Drafts/Outbox/Deleted/Junk), metadata for every arrival, bodies for
registered desk / specialist-sales senders (_data/sentiment/desk_senders.json), priority publications
(Substack incl. DAMNANG, SemiAnalysis, internal capstone.com.br forwards) and topic-matching subjects.

Writes to -OutputDirectory: mail.json (selected bodies, 12k-char cap), mail-metadata.json, mail-coverage.json
(window, counts, NEWEST RECEIVED timestamp — if that is far behind now, Outlook desktop is not syncing and the
task must switch to the M365 connector). Keep this file saved as UTF-8 WITH BOM (PowerShell 5.1).
Usage: powershell -NoProfile -ExecutionPolicy Bypass -File desk_mail_collect.ps1 -SinceUtc 2026-10-12T13:00:00Z -OutputDirectory <dir>
#>
param(
 [Parameter(Mandatory=$true)][string]$SinceUtc,
 [Parameter(Mandatory=$true)][string]$OutputDirectory
)
$ErrorActionPreference='Stop'
$since=[DateTimeOffset]::Parse($SinceUtc).UtcDateTime
$until=[DateTime]::UtcNow
[void][IO.Directory]::CreateDirectory($OutputDirectory)
$regPath=Join-Path $PSScriptRoot '..\_data\sentiment\desk_senders.json'
$registry=Get-Content -LiteralPath $regPath -Raw -Encoding UTF8 | ConvertFrom-Json
$known=@{}
foreach($p in $registry.senders.PSObject.Properties){$known[$p.Name.ToLowerInvariant()]=$p.Value}
$prioDomains=($registry.priority_domains | ForEach-Object {[regex]::Escape($_)}) -join '|'
$app=New-Object -ComObject Outlook.Application
$ns=$app.GetNamespace('MAPI')
$account=@($ns.Accounts | Where-Object {$_.SmtpAddress -ieq 'felipe.monteiro@capstone.com.br'})
if($account.Count -ne 1){throw 'Account felipe.monteiro@capstone.com.br unavailable or ambiguous in Outlook'}
$store=$account[0].DeliveryStore
$folders=[Collections.Generic.List[object]]::new()
function Walk-Mail($folder,$depth){
 if($depth -gt 5){return}
 if($folder.Name -match '^(Sent Items|Outbox|Drafts|Itens Enviados|Caixa de Sa.da|Rascunhos|Deleted Items|Itens Exclu.dos|Junk E.?mail|Lixo Eletr.nico|Sync Issues|Problemas de Sincroniza..o|Conversation History|Hist.rico de Conversas)$'){return}
 if($folder.DefaultItemType -eq 0){$folders.Add($folder)}
 foreach($child in $folder.Folders){Walk-Mail $child ($depth+1)}
}
Walk-Mail ($store.GetRootFolder()) 0
$inbox=$ns.GetDefaultFolder(6)
$newest=$null
try{$it=$inbox.Items;$it.Sort('[ReceivedTime]',$true);$f=$it.GetFirst();if($f){$newest=$f.ReceivedTime.ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')}}catch{}
$rows=[Collections.Generic.List[object]]::new();$metadata=[Collections.Generic.List[object]]::new();$audit=[Collections.Generic.List[object]]::new()
$seen=[Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
$cut='@SQL="urn:schemas:httpmail:datereceived" >= '''+$since.ToLocalTime().ToString('yyyy-MM-dd HH:mm')+''''
$topic='(?i)\b(semis?|semiconductor|software|internet|cloud|AI|cyber|networking|optical|optics|memory|HBM|DRAM|datacenter|data center|TMT|positioning|flows|crowded|sentiment|specialist|desk|axes?|color|colour|LITE|Lumentum|NVDA|Nvidia|META|MSFT|Microsoft|AMZN|Amazon|GOOG|Google|AMD|AVGO|Broadcom|MU|Micron|MRVL|Marvell|ANET|Arista|COHR|Coherent|CRWD|PANW|SNOW|ORCL|Oracle|TSM|TSMC|ASML|Hynix|Samsung|semianalysis|damnang|Anthropic|OpenAI|Jensen)\b'
$self='^(Sentiment Radar \||Twitter Briefing|Twitter Morning Wrap|Daily Analyst|Wiki )'
foreach($folder in $folders){
 try{$items=$folder.Items.Restrict($cut);$count=$items.Count}catch{$audit.Add(@{folder=$folder.FolderPath;error=$_.Exception.Message});continue}
 for($i=1;$i -le $count;$i++){
  $item=$items.Item($i)
  try{
   if($item.Class -ne 43){continue}
   $id=[string]$item.EntryID;if(-not $seen.Add($id)){continue}
   $sender=([string]$item.SenderEmailAddress).ToLowerInvariant()
   if($item.SenderEmailType -eq 'EX'){try{$sender=([string]$item.Sender.GetExchangeUser().PrimarySmtpAddress).ToLowerInvariant()}catch{}}
   $subject=[string]$item.Subject;$date=$item.ReceivedTime.ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
   if($subject -match $self){continue}
   $reason=if($known.ContainsKey($sender)){'registered desk sender'}elseif($sender -match $prioDomains){'priority publication or internal forward'}elseif($subject -match $topic){'topic subject'}else{'metadata only'}
   $reg=$known[$sender]
   $metadata.Add(@{id=$id;subject=$subject;sender=$sender;sender_name=[string]$item.SenderName;date=$date;selection=$reason;folder=$folder.FolderPath})
   if($reason -eq 'metadata only'){continue}
   $body=[string]$item.Body;if($body.Length -gt 12000){$body=$body.Substring(0,12000)+' [...]'}
   $rows.Add(@{id=$id;subject=$subject;sender=$sender;sender_name=[string]$item.SenderName;firm=$(if($reg){$reg[0]}else{$null});author=$(if($reg){$reg[1]}else{$null});role=$(if($reg){$reg[2]}else{$null});date=$date;body=$body;folder=$folder.FolderPath;attachments=$item.Attachments.Count;selection=$reason})
  }catch{$audit.Add(@{folder=$folder.FolderPath;item=$i;error=$_.Exception.Message})}
  finally{[void][Runtime.InteropServices.Marshal]::ReleaseComObject($item)}
 }
}
$enc=New-Object System.Text.UTF8Encoding($false)
[IO.File]::WriteAllText((Join-Path $OutputDirectory 'mail.json'),(ConvertTo-Json -InputObject @($rows.ToArray()) -Depth 6),$enc)
[IO.File]::WriteAllText((Join-Path $OutputDirectory 'mail-metadata.json'),(ConvertTo-Json -InputObject @($metadata.ToArray()) -Depth 5),$enc)
$lagH=$null;if($newest){$lagH=[math]::Round(($until-[DateTime]::Parse($newest).ToUniversalTime()).TotalHours,1)}
$coverage=@{channel='outlook-com';collected_utc=$until.ToString('yyyy-MM-ddTHH:mm:ssZ');since_utc=$since.ToString('yyyy-MM-ddTHH:mm:ssZ');newest_received_utc=$newest;inbox_lag_hours=$lagH;metadata_scanned=$metadata.Count;bodies_retrieved=$rows.Count;folders=$folders.Count;errors=@($audit.ToArray())}
[IO.File]::WriteAllText((Join-Path $OutputDirectory 'mail-coverage.json'),($coverage | ConvertTo-Json -Depth 6),$enc)
Write-Output ('desk mail: '+$metadata.Count+' metadata, '+$rows.Count+' bodies, newest received '+$newest+' (inbox lag '+$lagH+' h)')
