# Fetch e-mail bodies for the rows in sellside_mail_raw.json (by EntryID, Outlook COM) → JSONL {id, body}.
# Resumable and incremental: a companion ids index (.ids, one EntryID per line) is the fast "already fetched"
# set, so a nightly run only touches new mail instead of re-reading the ~400 MB JSONL. If the index is
# missing it is bootstrapped by scanning the JSONL once.
# Body truncated to -MaxChars (disclaimers and link farms live at the end anyway).
# Usage: powershell -File sellside_mail_bodies.ps1 [-MaxChars 9000]
param([string]$Raw = "E:\Wiki Felipe empresas\_wiki\_data\sentiment\sellside_mail_raw.json",
      [string]$Out = "E:\Wiki Felipe empresas\_wiki\_data\sentiment\sellside_mail_bodies.jsonl",
      [int]$MaxChars = 9000)
$ErrorActionPreference = 'SilentlyContinue'
$Ids = [System.IO.Path]::ChangeExtension($Out, '.ids')
$rows = Get-Content -Raw -Encoding UTF8 $Raw | ConvertFrom-Json
$done = @{}
if (Test-Path $Ids) {
  foreach ($line in [System.IO.File]::ReadLines($Ids)) { if ($line) { $done[$line] = 1 } }
  Write-Host ("ids index: " + $done.Count)
} elseif (Test-Path $Out) {
  Write-Host "no ids index — bootstrapping from the JSONL (one-off)"
  $sb = New-Object System.Text.StringBuilder
  foreach ($line in [System.IO.File]::ReadLines($Out)) {
    $i = $line.IndexOf('"id":"')
    if ($i -ge 0) { $j = $line.IndexOf('"', $i + 6); $id = $line.Substring($i + 6, $j - $i - 6); $done[$id] = 1; [void]$sb.AppendLine($id) }
  }
  [System.IO.File]::WriteAllText($Ids, $sb.ToString())
  Write-Host ("bootstrapped ids: " + $done.Count)
}
Write-Host ("rows=" + $rows.Count + " already=" + $done.Count)
$ol = New-Object -ComObject Outlook.Application
$ns = $ol.GetNamespace('MAPI')
$sw = [System.IO.StreamWriter]::new($Out, $true, [System.Text.UTF8Encoding]::new($false))
$iw = [System.IO.StreamWriter]::new($Ids, $true, [System.Text.UTF8Encoding]::new($false))
$n = 0; $fail = 0
foreach ($r in $rows) {
  $id = $r.id
  if (-not $id -or $done.ContainsKey($id)) { continue }
  $done[$id] = 1
  $it = $null; try { $it = $ns.GetItemFromID($id) } catch { $fail++; continue }
  if ($it -eq $null) { $fail++; continue }
  $b = ''; try { $b = $it.Body } catch {}
  if ($b -eq $null) { $b = '' }
  if ($b.Length -gt $MaxChars) { $b = $b.Substring(0, $MaxChars) }
  $o = [pscustomobject]@{ id = $id; body = $b }
  $sw.WriteLine(($o | ConvertTo-Json -Compress -Depth 2))
  $iw.WriteLine($id)
  $n++
  if ($n % 500 -eq 0) { $sw.Flush(); $iw.Flush(); Write-Host ("fetched=" + $n + " fail=" + $fail) }
  [System.Runtime.InteropServices.Marshal]::ReleaseComObject($it) | Out-Null
}
$sw.Flush(); $sw.Close(); $iw.Flush(); $iw.Close()
Write-Host ("DONE fetched=" + $n + " fail=" + $fail)
