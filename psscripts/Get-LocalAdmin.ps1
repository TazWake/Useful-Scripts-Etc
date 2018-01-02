<#
This script queries a remote machine to identify members of the local admin group on the remote machine.

Example use: Get-LocalAdminGroup "Remote Machine FQDN"

On a large domain this script can take a LONG time to complete
#>

function Get-LocalAdminGroup {param ($remotemachine) 
 
    $localadmins = Gwmi win32_groupuser –computer $remotemachine  
    $localadmins = $localadmins |? {$_.groupcomponent –like '*"Administrators"'} 
 
    $localadmins |% { 
        $_.partcomponent –match “.+Domain\=(.+)\,Name\=(.+)$” > $nul 
        $matches[1].trim('"') + “\” + $matches[2].trim('"') 
    } 
}

<# This block is if you have a text file with hostnames saved as Servers.txt #>
$Servers = gc .\Servers.txt

foreach ($s in $Servers)
{
    Write-Host $s
    $localadmins = Get-LocalAdminGroup $s 
    foreach ($admin in $localadmins)
    {
        $str = "$s,$admin"
        $str | Out-File .\AdminList.txt -Append
    }
}
