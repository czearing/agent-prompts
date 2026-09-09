param(
    [string]$CredentialTarget = "Paperclip.ReverbPriorityQueue",
    [Parameter(Mandatory)][string]$PythonPath
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
. "$PSScriptRoot\CredentialStore.ps1"

$configuration = Get-ReverbCredential -Target $CredentialTarget |
    ConvertFrom-Json
$env:REVERB_API_URL = $configuration.api_url
$env:REVERB_API_KEY = $configuration.api_key
$env:REVERB_COMPANY_ID = $configuration.company_id
$env:REVERB_RUN_ID = $configuration.run_id
$env:REVERB_AGENT_ID = $configuration.engineer_id

$cli = Join-Path (Split-Path $PSScriptRoot -Parent) "scripts\cli.py"
& $PythonPath $cli run-once
exit $LASTEXITCODE
