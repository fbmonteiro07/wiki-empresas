$ErrorActionPreference = 'Stop'
$taskWorkbook = Join-Path $PSScriptRoot '..\..\outputs\anthropic-2026-10-15\Anthropic_Financial_Model.xlsx'
$taskWorkbook = (Resolve-Path -LiteralPath $taskWorkbook).ProviderPath
$taskExcel = $null
$taskBook = $null
try {
  $taskExcel = New-Object -ComObject Excel.Application
  $taskExcel.Visible = $false
  $taskExcel.DisplayAlerts = $false
  $taskExcel.AskToUpdateLinks = $false
  $taskExcel.AutomationSecurity = 3
  $taskBook = $taskExcel.Workbooks.Open($taskWorkbook, 0, $true)
  $taskExcel.CalculateFullRebuild()
  $taskOps = $taskBook.Worksheets.Item('Operating')
  $taskDrivers = $taskBook.Worksheets.Item('Drivers')
  $taskCash = $taskBook.Worksheets.Item('Cash flow')
  $taskReport = [ordered]@{engine=$taskExcel.Version; readonly=$taskBook.ReadOnly; base2030=$taskOps.Range('J31').Value2; sensitivityBase=$taskDrivers.Range('I57').Value2; sensitivityCorner=$taskDrivers.Range('G55').Value2; secondTableBase=$taskDrivers.Range('I67').Value2; cashMissing=$taskCash.Range('J21').Value2}
  if ([math]::Abs($taskReport.base2030 - (-20415.22148801462)) -gt 0.01) { throw 'Native base mismatch' }
  if ([math]::Abs($taskReport.sensitivityBase - $taskReport.base2030) -gt 0.01) { throw 'Native first table mismatch' }
  if ([math]::Abs($taskReport.secondTableBase - $taskReport.base2030) -gt 0.01) { throw 'Native second table mismatch' }
  $taskSummary = $taskBook.Worksheets.Item('Summary')
  $taskCompute = $taskBook.Worksheets.Item('Compute')
  $taskReport.revenuePerInferenceGW2026USDbn = $taskSummary.Range('F26').Value2
  $taskReport.costPerDirectGW2026USDbn = $taskSummary.Range('F27').Value2
  if ([math]::Abs($taskReport.revenuePerInferenceGW2026USDbn - 69.44444444444442) -gt 0.000001) { throw 'Native revenue/GW mismatch' }
  if ([math]::Abs($taskReport.costPerDirectGW2026USDbn - 13.43304351348158) -gt 0.000001) { throw 'Native cost/GW mismatch' }
  foreach ($taskColumn in @('E','F','G','H','I','J')) {
    $taskExpectedCostGW = $taskCompute.Range($taskColumn + '21').Value2 / $taskCompute.Range($taskColumn + '29').Value2 / 1000
    if ([math]::Abs($taskSummary.Range($taskColumn + '27').Value2 - $taskExpectedCostGW) -gt 0.000001) { throw 'Native cost/GW annual bridge mismatch' }
  }
  $taskReport.infeasibleSensitivity = $taskDrivers.Range('G59').Value2
  if ($taskReport.infeasibleSensitivity -ne 'n.a.') { throw 'Native capacity guard failed' }
  $taskSelectedFormula = $taskDrivers.Range('J36').Formula
  $taskDrivers.Range('J36').ClearContents()
  $taskExcel.CalculateFullRebuild()
  if ([math]::Abs($taskOps.Range('J31').Value2 - $taskReport.base2030) -gt 0.01) { throw 'Unselected blank affected base' }
  $taskDrivers.Range('E4').Value2 = 2
  $taskExcel.CalculateFullRebuild()
  $taskReport.selectedMissingInput = $taskDrivers.Range('J34').Value2
  if ($taskReport.selectedMissingInput -ne 'n.a.') { throw 'Native selected blank coerced to zero' }
  $taskDrivers.Range('J36').Formula = $taskSelectedFormula
  $taskDrivers.Range('E4').Value2 = 1
  $taskDrivers.Range('G5').Value2 = -0.05
  $taskExcel.CalculateFullRebuild()
  $taskReport.share20pct = $taskOps.Range('J31').Value2
  if ([math]::Abs($taskReport.share20pct - 209.77851198538) -gt 0.01) { throw 'Native share sensitivity mismatch' }
  $taskDrivers.Range('G5').Value2 = 0
  $taskDrivers.Range('E4').Value2 = 2
  $taskExcel.CalculateFullRebuild()
  $taskReport.downside2030 = $taskOps.Range('J31').Value2
  $taskReport.historyUnchanged = $taskOps.Range('E31').Value2
  $taskDrivers.Range('E4').Value2 = 1
  $taskCash.Range('J12:J19').Value2 = 0
  $taskExcel.CalculateFullRebuild()
  $taskReport.cashZeroInputs = $taskCash.Range('J21').Value2
  if ([math]::Abs($taskReport.cashZeroInputs - $taskReport.base2030) -gt 0.01) { throw 'Native zero cash inputs mismatch' }
  $taskReport.status = 'PASS'
  $taskReport | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'native_excel_checks.json') -Encoding utf8
  $taskReport | ConvertTo-Json
} finally {
  if ($null -ne $taskBook) { $taskBook.Close($false) }
  if ($null -ne $taskExcel) { $taskExcel.Quit() }
}
