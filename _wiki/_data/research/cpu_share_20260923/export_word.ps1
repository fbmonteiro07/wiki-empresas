$ErrorActionPreference = 'Stop'
$cpuDocPath = 'E:\Wiki Felipe empresas\_deliverables\CPU_market_share_2021_2030_2026-09-23.docx'
$cpuPdfPath = 'E:\Wiki Felipe empresas\_wiki\_data\research\cpu_share_20260923\word_render.pdf'
$cpuWord = $null
$cpuDocument = $null
try {
    $cpuWord = New-Object -ComObject Word.Application
    $cpuWord.Visible = $false
    $cpuWord.DisplayAlerts = 0
    $cpuDocument = $cpuWord.Documents.Open($cpuDocPath, $false, $true)
    $cpuDocument.Repaginate()
    $cpuDocument.ExportAsFixedFormat($cpuPdfPath, 17)
    Write-Output ('Rendered pages: ' + $cpuDocument.ComputeStatistics(2))
    Write-Output $cpuPdfPath
} finally {
    if ($null -ne $cpuDocument) { $cpuDocument.Close(0) }
    if ($null -ne $cpuWord) { $cpuWord.Quit() }
}
