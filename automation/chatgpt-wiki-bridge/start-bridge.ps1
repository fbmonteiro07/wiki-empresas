param(
    [switch]$Install
)

$ErrorActionPreference = "Stop"

$bridgeDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$bridge = Join-Path $bridgeDir "bridge.py"

if ($Install) {
    $runKey = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
    $command = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$($MyInvocation.MyCommand.Path)`""
    New-Item -Path $runKey -Force | Out-Null
    New-ItemProperty -Path $runKey -Name "ChatGPTWikiBridge" -Value $command -PropertyType String -Force | Out-Null
}

$logDir = Join-Path $bridgeDir "state"
$stdout = Join-Path $logDir "bridge.stdout.log"
$stderr = Join-Path $logDir "bridge.stderr.log"

New-Item -ItemType Directory -Force -Path $logDir | Out-Null

$existing = Get-CimInstance Win32_Process -Filter "Name = 'python.exe' OR Name = 'py.exe'" |
    Where-Object { $_.CommandLine -and $_.CommandLine.Contains($bridge) }
if ($existing) {
    exit 0
}

$launcher = Get-Command py.exe -ErrorAction SilentlyContinue
if ($launcher) {
    Start-Process -FilePath $launcher.Source -ArgumentList @("-3", "`"$bridge`"") `
        -WindowStyle Hidden -RedirectStandardOutput $stdout -RedirectStandardError $stderr
    exit 0
}

$python = Get-Command python.exe -ErrorAction SilentlyContinue
if (-not $python) {
    throw "Python was not found. Install Python or add py.exe/python.exe to PATH."
}
Start-Process -FilePath $python.Source -ArgumentList @("`"$bridge`"") `
    -WindowStyle Hidden -RedirectStandardOutput $stdout -RedirectStandardError $stderr
