# This is a simple script to collect IR data
# Copied from Investigate Like a Rockstar

Write-host "[+} Commencing data collection..." - foregroundcolor white
date | out-file -append ".\hash.txt"

# Collect general information
Systeminfo | out-file -append ".\results.txt"

#Networking
Ipconfig /all | out-file -append ".\results.txt"

#Local Users
Net user | out-file -append ".\results.txt"

#Networking
Netstat -nao | out-file -append ".\results.txt"

#Process list from pstree
.\pstree.ps1

#Journal Entry
Wevtutil epl security .\security.evtx

#Hash Results
Get-FileHash ".\results.txt" | Format-List | out-file -append ".\hash.txt"
Get-FileHash ".\security.evtx" | Format-List | out-file -append ".\hash.txt"

Write-host "[+] Collection over" -foregroundcolor white
