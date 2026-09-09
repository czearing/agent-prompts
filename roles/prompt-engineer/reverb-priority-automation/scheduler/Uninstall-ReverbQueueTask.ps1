param(
    [string]$TaskName = "Paperclip-Reverb-Priority-Queue",
    [string]$CredentialTarget = "Paperclip.ReverbPriorityQueue"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
. "$PSScriptRoot\CredentialStore.ps1"

if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}
Remove-ReverbCredential -Target $CredentialTarget
