# This is a quick script to check for vulnerable accounts on a network
# It relies on UserRights.ps1 - https://gallery.technet.microsoft.com/scriptcenter/Grant-Revoke-Query-user-26e259b0

Import-Module .\UserRights.ps1 
Get-AccountsWithUserRight -Right SeBackupPrivilege
Get-AccountsWithUserRight -Right SeDebugPrivilege
