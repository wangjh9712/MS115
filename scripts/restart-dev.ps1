param(
    [string]$HostAddress = "0.0.0.0",
    [int]$FrontendPort = 5173,
    [int]$BackendPort = 8000
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$frontendDir = Join-Path $repoRoot "frontend"
$backendDir = Join-Path $repoRoot "backend"
$venvPython = Join-Path $backendDir "venv\\Scripts\\python.exe"
$npmCmd = "C:\\Program Files\\nodejs\\npm.cmd"

if (-not (Test-Path $venvPython)) {
    throw "Backend Python not found: $venvPython"
}

if (-not (Test-Path $npmCmd)) {
    throw "npm.cmd not found: $npmCmd"
}

$listenPorts = @($FrontendPort, $BackendPort)
$pidsToStop = Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue |
    Where-Object { $_.LocalPort -in $listenPorts } |
    Select-Object -ExpandProperty OwningProcess -Unique

foreach ($processId in $pidsToStop) {
    try {
        Stop-Process -Id $processId -Force -ErrorAction Stop
    } catch {
        Write-Warning "Failed to stop PID ${processId}: $($_.Exception.Message)"
    }
}

Start-Sleep -Seconds 1

Start-Process -FilePath $venvPython `
    -ArgumentList "-m uvicorn main:app --host $HostAddress --port $BackendPort --reload" `
    -WorkingDirectory $backendDir | Out-Null

Start-Process -FilePath $npmCmd `
    -ArgumentList "run dev -- --host $HostAddress --port $FrontendPort" `
    -WorkingDirectory $frontendDir | Out-Null

Start-Sleep -Seconds 3

$listeners = Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue |
    Where-Object { $_.LocalPort -in $listenPorts } |
    Select-Object LocalAddress, LocalPort, OwningProcess |
    Sort-Object LocalPort

if (($listeners | Measure-Object).Count -lt 2) {
    throw "Restart attempted, but one or more ports are not listening yet (expected: $($listenPorts -join ', '))."
}

Write-Host "Restart complete."
$listeners | Format-Table -AutoSize
