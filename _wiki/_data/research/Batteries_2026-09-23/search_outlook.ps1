$ErrorActionPreference = 'Stop'
$outPath = Join-Path $PSScriptRoot 'emails_live.jsonl'
$ol = New-Object -ComObject Outlook.Application
$ns = $ol.GetNamespace('MAPI')
$folders = New-Object System.Collections.ArrayList
function Walk($folder, $depth) {
    if ($depth -gt 8) { return }
    $name = $folder.Name
    if ($name -match '^(Deleted Items|Junk Email|Sent Items|Drafts|Outbox|Itens Excluídos|Lixo Eletrônico|Itens Enviados|Rascunhos)$') { return }
    if ($folder.DefaultItemType -eq 0) { [void]$folders.Add($folder) }
    for ($i = 1; $i -le $folder.Folders.Count; $i++) { Walk $folder.Folders.Item($i) ($depth + 1) }
}
for ($i = 1; $i -le $ns.Folders.Count; $i++) { Walk $ns.Folders.Item($i) 0 }
$keywords = @('battery','batteries','bateria','BESS','BBU','lithium','LFP','CATL','Megapack','Powerwall','Fluence','FLNC','energy storage','sodium','solid-state','anode','cathode','Albemarle','QuantumScape','Enovix','Amprius','Gotion','Sunwoda','LG Energy','Samsung SDI','SK On','Panasonic','AES','Eos Energy','Form Energy')
$parts = ($keywords | ForEach-Object { '"urn:schemas:httpmail:subject" LIKE ' + "'%$_%'" }) -join ' OR '
$filter = '@SQL=("urn:schemas:httpmail:datereceived" >= ''2026-06-25 00:00'') AND ("urn:schemas:httpmail:datereceived" < ''2026-09-24 00:00'') AND (' + $parts + ')'
$writer = [System.IO.StreamWriter]::new($outPath, $false, [System.Text.UTF8Encoding]::new($false))
$seen = @{}; $total = 0; $errors = 0
try {
 foreach ($folder in $folders) {
    try { $items = $folder.Items.Restrict($filter); $count = $items.Count } catch { Write-Host ('FILTER_ERROR|' + $folder.FolderPath + '|' + $_.Exception.Message); $errors++; continue }
    Write-Host ('FOLDER|' + $folder.FolderPath + '|' + $count)
    $item = $items.GetFirst()
    while ($null -ne $item) {
      try {
        if ($item.Class -eq 43 -and -not $seen.ContainsKey($item.EntryID)) {
            $seen[$item.EntryID] = 1
            $attachments = @(); for ($a=1; $a -le $item.Attachments.Count; $a++) { $attachments += $item.Attachments.Item($a).FileName }
            $record = [pscustomobject]@{id=$item.EntryID; d=$item.ReceivedTime.ToString('yyyy-MM-dd'); t=$item.ReceivedTime.ToString('HH:mm'); sender=$item.SenderName; from=$item.SenderEmailAddress; subject=$item.Subject; folder=$folder.FolderPath; body=$item.Body; attachments=$attachments}
            $writer.WriteLine(($record | ConvertTo-Json -Depth 4 -Compress)); $total++
            if ($total % 100 -eq 0) { $writer.Flush(); Write-Host ('FETCHED|' + $total) }
        }
      } catch { $errors++ }
      $item = $items.GetNext()
    }
 }
} finally { $writer.Flush(); $writer.Close() }
Write-Host ('DONE|total=' + $total + '|errors=' + $errors)
