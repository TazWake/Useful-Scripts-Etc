# Grab the Security Event Log
wevtutil epl security .\security.evtx

# quick review of evtx for obvious badness
Get-WinEvent -FilterHashtable @{path='.\security.evtx';id=4624}` | Select-Object -Property timecreated,id, @{label='username';expression={$_.properties[5].value}}, @{label='domain';expression={$_.properties[6].value}}, @{label='Source';expression={$_.properties[18].value}} | export-csv review_events_4624.csv
Get-WinEvent -FilterHashtable @{path='.\security.evtx';id=4648}` | Select-Object -Property timecreated,id, @{label='username';expression={$_.properties[5].value}}, @{label='domain';expression={$_.properties[6].value}}, @{label='Source';expression={$_.properties[12].value}} | export-csv review_events_4648.csv
Get-WinEvent -FilterHashtable @{path='.\security.evtx';id=4672}` | Select-Object -Property timecreated,id, @{label='username';expression={$_.properties[1].value}},@{label='Domain';expression={$_.properties[2].value}} | export-csv review_events_4672.csv
