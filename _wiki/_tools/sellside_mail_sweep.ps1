# Sell-side e-mail sweep for the sentiment indicator (subject-level, store-side DASL filtering — never per-item iteration).
# Writes one JSON row per broker e-mail: received date/time, sender e-mail, subject, folder, EntryID.
#
# Nightly (incremental — what the scheduled task runs): sweep the last N days into a DELTA file,
# then `py build_sentiment.py --step mail_merge` folds it into sellside_mail_raw.json.
#   powershell -File sellside_mail_sweep.ps1 -Days 7 -Out ...\sellside_mail_delta.json
# Full rebuild (~9 min, the whole retained mailbox):
#   powershell -File sellside_mail_sweep.ps1 -Since 2026-01-31 -Out ...\sellside_mail_raw.json
#
# -Days wins over -Since when both are given. Mailbox retention starts 2026-01-31; earlier is not recoverable.
param([int]$Days = 0,
      [string]$Since = '2026-01-31',
      [string]$Out = "E:\Wiki Felipe empresas\_wiki\_data\sentiment\sellside_mail_delta.json")
$ErrorActionPreference = 'SilentlyContinue'
if ($Days -gt 0) { $Since = (Get-Date).AddDays(-$Days).ToString('yyyy-MM-dd') }
Write-Host ("SWEEP since=" + $Since + " out=" + $Out)
$ol = New-Object -ComObject Outlook.Application
$ns = $ol.GetNamespace('MAPI')
$folders = New-Object System.Collections.ArrayList
function Walk($f, $d) {
  if ($d -gt 4) { return }
  try { if ($f.DefaultItemType -eq 0) { $n = $f.Name.ToLower(); if ($n -notmatch 'deleted|junk|sent|drafts|outbox|lixo|excluídos|enviados|rascunhos|spam') { [void]$folders.Add($f) } } } catch {}
  try { for ($i = 1; $i -le $f.Folders.Count; $i++) { Walk $f.Folders.Item($i) ($d + 1) } } catch {}
}
for ($s = 1; $s -le $ns.Folders.Count; $s++) { Walk $ns.Folders.Item($s) 0 }
$doms = @('morganstanley', 'jefferies', 'bofa', 'ubs.com', 'ubsbb', 'jpmorgan', 'jpmresearchmail', 'jpmchase', 'gs.com', 'bernstein', 'barclays', 'citi.com', 'db.com', 'sig.com',
          'rothschildandco', 'wolferesearch', 'evercore', 'needham', 'raymondjames', 'stifel', 'mizuho', 'tdcowen', 'cowen.com', 'wellsfargo', 'bmo.com', 'rbccm', 'baird', 'piper',
          'oppenheimer', 'kbw', 'loopcapital', 'rosenblatt', 'newstreetresearch', 'arete', 'melius', 'moffettnathanson', 'btig', 'craig-hallum', 'benchmark', 'cantor', 'hsbc', 'bnpparibas',
          'exanebnpparibas', 'macquarie', 'nomura', 'daiwa', 'clsa', 'jefferies.com', 'guggenheim', 'truist', 'keybanc', 'wedbush', 'susquehanna', 'northlandcapital', 'bankofamerica', 'ml.com',
          'redburn', 'kepler', 'berenberg', 'santander', 'itau', 'btgpactual', 'xpi.com', 'bradesco')
$fe = 'urn:schemas:httpmail:fromemail'
$parts = ($doms | ForEach-Object { '"' + $fe + '" LIKE ' + "'%$_%'" }) -join ' OR '
$dasl = '@SQL=("urn:schemas:httpmail:datereceived" >= ''' + $Since + ' 00:00'') AND (' + $parts + ')'
$rows = New-Object System.Collections.ArrayList
$seen = @{}
foreach ($f in $folders) {
  $r = $null; try { $r = $f.Items.Restrict($dasl) } catch { continue }
  $c = 0; try { $c = $r.Count } catch { continue }
  if ($c -eq 0) { continue }
  Write-Host ("FOLDER|" + $f.FolderPath + "|" + $c)
  $it = $r.GetFirst()
  while ($it -ne $null) {
    $subjv = ''; try { $subjv = $it.Subject } catch {}
    $rt = $null; try { $rt = $it.ReceivedTime } catch {}
    $se = ''; try { $se = $it.SenderEmailAddress } catch {}
    $id = ''; try { $id = $it.EntryID } catch {}
    if ($rt -ne $null -and $subjv -ne '') {
      $key = $rt.ToString('yyyyMMddHHmm') + '|' + $subjv
      if (-not $seen.ContainsKey($key)) {
        $seen[$key] = 1
        [void]$rows.Add([pscustomobject]@{ d = $rt.ToString('yyyy-MM-dd'); t = $rt.ToString('HH:mm'); from = $se; subject = $subjv; folder = $f.Name; id = $id })
      }
    }
    $it = $r.GetNext()
  }
}
Write-Host ("TOTAL=" + $rows.Count)
# ConvertTo-Json collapses a 1-element array to an object; the Python side accepts both.
$rows | ConvertTo-Json -Depth 3 -Compress | Out-File -Encoding utf8 $Out
Write-Host ("WROTE " + $Out)
