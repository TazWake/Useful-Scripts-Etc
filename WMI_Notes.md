#Using WMIC

##Some example commands to assist DFIR

Killing running processes by PID

```
wmic process where processid=[pid] call terminate
```

Killing running processes by NAME
```
wmic process where name="evilprocess.exe" call terminate
```
