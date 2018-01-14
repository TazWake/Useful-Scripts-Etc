# Powershell script using Accesschk from Sysinternals to hunt for user privileges.

gwmi Win32_UserProfile | foreach-object {
    # Set up containers
    $sid = New-Object System.Security.Principal.SecurityIdentifier($_.SID)
    $user = $sid.Translate([System.Security.Principal.NTAccount])
    $username = $user.Value

    # Display Username
    $username
    $chkCmd = ".\accesschk.exe """ + $username + """ -a * -q"
    iex $chkCmd
    ""
/
    # TODO Identify a way to parse the output and flag SeBackupPrivilege and SeDebugPrivilege
}
