$ErrorActionPreference = 'Stop'
$outDir = $PSScriptRoot
$ol = New-Object -ComObject Outlook.Application
$ns = $ol.GetNamespace('MAPI')
$folders = New-Object System.Collections.ArrayList
function Walk($folder, $depth) {
  if ($depth -gt 8 -or $folder.Name -match '^(Deleted Items|Junk Email|Sent Items|Drafts|Outbox|Itens Excluídos|Lixo Eletrônico|Itens Enviados|Rascunhos)$') { return }
  if ($folder.DefaultItemType -eq 0) { [void]$folders.Add($folder) }
  for ($i=1; $i -le $folder.Folders.Count; $i++) { Walk $folder.Folders.Item($i) ($depth+1) }
}
for ($i=1; $i -le $ns.Folders.Count; $i++) { Walk $ns.Folders.Item($i) 0 }
$filter = '@SQL=("urn:schemas:httpmail:datereceived" >= ''2026-09-01 00:00'') AND ("urn:schemas:httpmail:subject" LIKE ''%semicon%'' OR "urn:schemas:httpmail:subject" LIKE ''%semiwest%'' OR "urn:schemas:httpmail:textdescription" LIKE ''%semicon west%'' OR "urn:schemas:httpmail:textdescription" LIKE ''%semiwest%'')'
$writer = [System.IO.StreamWriter]::new((Join-Path $outDir 'emails_live.jsonl'),$false,[System.Text.UTF8Encoding]::new($false))
$seen=@{}; $total=0; $errors=0
try {
 foreach ($folder in $folders) {
  try { $items=$folder.Items.Restrict($filter); $count=$items.Count } catch { Write-Host ('FILTER_ERROR|'+$folder.FolderPath+'|'+$_.Exception.Message);$errors++;continue }
  Write-Host ('FOLDER|'+$folder.FolderPath+'|'+$count)
  $item=$items.GetFirst()
  while ($null -ne $item) {
   try {
    if ($item.Class -eq 43 -and -not $seen.ContainsKey($item.EntryID)) {
     $seen[$item.EntryID]=$true
     $attachments=@();for ($a=1;$a -le $item.Attachments.Count;$a++) { $att=$item.Attachments.Item($a);$attachments+=@{index=$a;name=$att.FileName;size=$att.Size} }
     $record=@{id=$item.EntryID;store_id=$folder.StoreID;d=$item.ReceivedTime.ToString('yyyy-MM-dd');t=$item.ReceivedTime.ToString('HH:mm');sender=$item.SenderName;from=$item.SenderEmailAddress;subject=$item.Subject;folder=$folder.FolderPath;body=$item.Body;html=$item.HTMLBody;attachments=$attachments}
     $writer.WriteLine(($record|ConvertTo-Json -Depth 5 -Compress));$writer.Flush();$total++
    }
   } catch { Write-Host ('ITEM_ERROR|'+$_.Exception.Message);$errors++ }
   $item=$items.GetNext()
  }
 }
} finally { $writer.Close() }
Write-Host ('DONE|total='+$total+'|errors='+$errors)
