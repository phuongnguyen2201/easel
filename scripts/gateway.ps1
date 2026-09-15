$ErrorActionPreference = 'Stop'
# NOTE: $Profile is a PowerShell automatic variable (path to the profile
# script). Shadowing it breaks anything that reads it later in the session, so
# this script uses $EaselProfile for the OpenClaw profile name.
$EaselProfile = 'easel'
$Root = Split-Path -Parent $PSScriptRoot
$LogFile = Join-Path $env:TEMP 'easel-gateway.log'
$ErrorLogFile = Join-Path $env:TEMP 'easel-gateway.error.log'
$ConfigDir = Join-Path $HOME ".openclaw-$EaselProfile"

# Gateway port - same resolution order as easel/gateway_port.py and
# scripts/gateway.sh: EASEL_GATEWAY_PORT env -> OPENCLAW_PORT in .env -> 18789.
# Must match gateway.port in ~/.openclaw-easel/openclaw.json, which is where
# `openclaw --profile easel agent` connects. Change both or neither:
#   openclaw --profile easel config set gateway.port <port>
$Port = $env:EASEL_GATEWAY_PORT
if (-not $Port) {
    $portMatch = Select-String -Path (Join-Path $Root '.env') -Pattern '^OPENCLAW_PORT=(.*)$' -ErrorAction SilentlyContinue |
        Select-Object -Last 1
    if ($portMatch) { $Port = $portMatch.Matches[0].Groups[1].Value }
}
$Port = "$Port".Trim().Trim('"').Trim("'")
if ($Port -notmatch '^\d+$') { $Port = '18789' }

function Test-Gateway {
    try { Invoke-WebRequest "http://127.0.0.1:$Port/healthz" -UseBasicParsing -TimeoutSec 2 | Out-Null; return $true }
    catch { return $false }
}

function Get-GatewayProcess {
    Get-CimInstance Win32_Process -Filter "Name = 'node.exe'" |
        Where-Object { $_.CommandLine -match "openclaw.*--profile\s+$EaselProfile.*gateway" } |
        Select-Object -First 1
}

function Stop-Gateway {
    $process = Get-GatewayProcess
    if ($process) { Stop-Process -Id $process.ProcessId -Force; Write-Host '[easel] Gateway stopped' }
    else { Write-Host '[easel] Gateway was not running' }
}

switch ($args[0]) {
    'start' {
        if (Test-Gateway) { Write-Host '[easel] Gateway already running'; break }
        New-Item -ItemType Directory -Force -Path $ConfigDir | Out-Null
        Write-Host "[easel] Starting Easel gateway (profile: $EaselProfile, port: $Port)..."
        $command = "openclaw --profile $EaselProfile gateway run --force --allow-unconfigured --bind loopback --port $Port"
        Start-Process powershell -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-Command', $command `
            -WorkingDirectory $Root -RedirectStandardOutput $LogFile -RedirectStandardError $ErrorLogFile -WindowStyle Hidden | Out-Null
        $ready = $false
        1..20 | ForEach-Object {
            if (-not $ready) {
                if (Test-Gateway) { $ready = $true }
                else { Start-Sleep -Seconds 1 }
            }
        }
        if ($ready) { Write-Host '[easel] Gateway started' }
        else { Write-Error "Gateway 启动失败；请检查 $LogFile 和 $ErrorLogFile"; exit 1 }
    }
    'stop' { Stop-Gateway }
    'restart' { Stop-Gateway; Start-Sleep -Seconds 2; & $PSCommandPath start }
    'status' {
        if (Test-Gateway) { Write-Host "[easel] Gateway running (profile: $EaselProfile, port: $Port)" }
        else { Write-Host '[easel] Gateway not running' }
    }
    'logs' { Get-Content $LogFile -Wait }
    'port' { Write-Host $Port }
    default { Write-Host 'Usage: gateway.ps1 {start|stop|restart|status|logs|port}'; exit 1 }
}
