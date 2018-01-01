# quick review of evtx for obvious badness
Get-WinEvent -FilterHashtable @{path='.\security.evtx';id=4624,4648,4672}
