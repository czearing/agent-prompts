param(
    [string]$TaskName = "Paperclip-Reverb-Priority-Queue",
    [string]$CredentialTarget = "Paperclip.ReverbPriorityQueue"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
. "$PSScriptRoot\CredentialStore.ps1"

$required = @(
    "PAPERCLIP_API_URL",
    "PAPERCLIP_API_KEY",
    "PAPERCLIP_COMPANY_ID",
    "PAPERCLIP_RUN_ID",
    "PAPERCLIP_AGENT_ID"
)
foreach ($name in $required) {
    if (-not [Environment]::GetEnvironmentVariable($name)) {
        throw "Missing required environment variable $name"
    }
}

$allowedEngineerId = "32cdb55f-fa10-40f3-929d-cf50b4dc3e10"
if ($env:PAPERCLIP_AGENT_ID -ne $allowedEngineerId) {
    throw "PAPERCLIP_AGENT_ID is not in the exact-id allowlist"
}

$configuration = @{
    api_url = $env:PAPERCLIP_API_URL
    api_key = $env:PAPERCLIP_API_KEY
    company_id = $env:PAPERCLIP_COMPANY_ID
    run_id = $env:PAPERCLIP_RUN_ID
    engineer_id = $env:PAPERCLIP_AGENT_ID
} | ConvertTo-Json -Compress
Set-ReverbCredential -Target $CredentialTarget -Payload $configuration

$launcher = Join-Path $PSScriptRoot "Run-ReverbQueue.ps1"
$powerShell = Join-Path $PSHOME "powershell.exe"
$python = (Get-Command python.exe -ErrorAction Stop).Source
$arguments = '-NoProfile -NonInteractive -ExecutionPolicy Bypass -File "' +
    $launcher + '" -CredentialTarget "' + $CredentialTarget +
    '" -PythonPath "' + $python + '"'
$action = New-ScheduledTaskAction -Execute $powerShell -Argument $arguments
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) `
    -RepetitionInterval (New-TimeSpan -Minutes 5)
$settings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew `
    -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 4)

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger `
    -Settings $settings -Description "Run deterministic reverb queue dispatch." `
    -Force | Out-Null
Enable-ScheduledTask -TaskName $TaskName | Out-Null

Get-ScheduledTask -TaskName $TaskName
