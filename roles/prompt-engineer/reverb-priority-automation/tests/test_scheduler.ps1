$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$scheduler = Join-Path (Split-Path $PSScriptRoot -Parent) "scheduler"
$install = Join-Path $scheduler "Install-ReverbQueueTask.ps1"
$uninstall = Join-Path $scheduler "Uninstall-ReverbQueueTask.ps1"
$suffix = [Guid]::NewGuid().ToString("N")
$primary = "ReverbQueueTest-$suffix"
$sibling = "$primary-Sibling"
$primaryCredential = "$primary-Credential"
$siblingCredential = "$sibling-Credential"

try {
    & $install -TaskName $primary -CredentialTarget $primaryCredential | Out-Null
    & $install -TaskName $primary -CredentialTarget $primaryCredential | Out-Null
    & $install -TaskName $sibling -CredentialTarget $siblingCredential | Out-Null

    $tasks = @(Get-ScheduledTask -TaskName $primary)
    if ($tasks.Count -ne 1) {
        throw "Expected one task after two installs; found $($tasks.Count)"
    }
    if ($tasks[0].State -eq "Disabled") {
        throw "Installed task is disabled"
    }
    $interval = $tasks[0].Triggers[0].Repetition.Interval
    if ($interval -ne "PT5M") {
        throw "Expected PT5M repetition; found $interval"
    }
    if ($tasks[0].Actions[0].Arguments.Contains($env:PAPERCLIP_API_KEY)) {
        throw "Task arguments expose the API credential"
    }
    if (-not $tasks[0].Actions[0].Arguments.Contains("Run-ReverbQueue.ps1")) {
        throw "Task action does not invoke the deterministic launcher"
    }

    & $uninstall -TaskName $primary -CredentialTarget $primaryCredential
    if (Get-ScheduledTask -TaskName $primary -ErrorAction SilentlyContinue) {
        throw "Uninstall left the requested task registered"
    }
    if (-not (Get-ScheduledTask -TaskName $sibling -ErrorAction SilentlyContinue)) {
        throw "Uninstall removed a different task"
    }
    "Scheduler installer assertions passed."
}
finally {
    & $uninstall -TaskName $primary -CredentialTarget $primaryCredential
    & $uninstall -TaskName $sibling -CredentialTarget $siblingCredential
}
