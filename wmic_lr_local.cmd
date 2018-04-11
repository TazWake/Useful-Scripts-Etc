@echo off
REM ############################################################################
REM # Windows Management Instrumentation Commandline Live Response
REM # By Justin Hall, justin.hall@cbts.cinbell.com
REM # Released under Creative Commons Attribution-Share Alike 3.0 US License
REM # see http://creativecommons.org/licenses/by-sa/3.0/us/ for details
REM ############################################################################

echo Beginning Live Response...
echo.

REM Autorun entries
echo Getting startup entries...
wmic startup get caption,command,location /format:list > startup.txt
echo Results written to startup.txt
echo.

REM Logon sessions
echo Getting login sessions...
wmic netlogin get name,description,lastlogon,lastlogoff,numberoflogons,passwordage,usertype,workstations /format:list > netlogin.txt
echo Results written to netlogin.txt
echo.

REM Event logs
REM NOTE: This can be a large dataset for a Windows install that's been around a while.
REM You may want to specify individual eventcodes for particular events you want.
REM Example: wmic ntevent where (logfile="security" AND (eventcode="529" OR eventcode="540")) list brief
set choice=
set /p choice="Do you want to get event logs? This could take a while. Enter y or n: "
if '%choice%'=='n' goto skip
if '%choice%'=='y' goto noskip
echo.

:noskip
echo Getting event logs...
wmic ntevent where (logfile="system") list brief > eventlog_system.txt
wmic ntevent where (logfile="security") list brief > eventlog_security.txt
wmic ntevent where (logfile="application") list brief > eventlog_app.txt
echo Results written to eventlog_system.txt, eventlog_security.txt, and eventlog_app.txt
echo.

:skip
REM List of drivers
echo Getting list of drivers...
wmic sysdriver list full > drivers.txt
echo Results written to drivers.txt
echo.

REM List of mapped network drives
echo Getting list of mapped network drives...
wmic netuse list full > mappeddrives.txt
echo Results written to mappeddrives.txt
echo.

REM List of running processes
echo Getting list of running processes...
wmic process get Name,Description,CommandLine,ProcessId,ThreadCount,Handle,HandleCount /format:list > process.txt
echo Results written to process.txt
echo.

REM Scheduled tasks with AT command
echo Getting list of "AT" scheduled tasks...
wmic job list full > jobs.txt
echo Results written to jobs.txt
echo.

REM Services
echo Getting list of services...
wmic service list full > services.txt
echo Results written to services.txt
echo.

REM Environment variables
echo Getting list of environment variables...
wmic environment get name,username,variablevalue,systemvariable /format:list > environment_variables.txt
echo Results written to environment_variables.txt
echo.

REM Local user accounts
echo Getting list of local user accounts...
wmic useraccount where (localaccount="TRUE") get caption,domain,name,fullname,sid,lockout,passwordexpires,passwordrequired,status /format:list > useraccounts.txt
echo . >> useraccounts.txt
wmic sysaccount list brief >> useraccounts.txt
echo Results written to useraccounts.txt
echo.

REM Local groups
echo Getting list of local groups...
wmic group where (localaccount="TRUE") list full > groups.txt
echo Results written to groups.txt
echo.

REM Logged in user
echo Getting logged-in user...
wmic computersystem get username > username.txt
echo Results written to username.txt
echo.

REM Network configuration
echo Getting network configuration...
wmic nicconfig where IPEnabled="TRUE" get DefaultIPGateway,Description,DHCPEnabled,DHCPLeaseExpires,DHCPLeaseObtained,DHCPServer,DNSDomain,DNSDomainSuffixSearchOrder,DNSHostName,IPAddress,IPSubnet,MACAddress,ServiceName,WINSPrimaryServer,WinsSecondaryServer /format:list > network_config.txt
echo Results written to network_config.txt
echo.

REM Files opened remotely by others via share
echo Getting shares...
wmic share get description,name,path /format:list > shares.txt
echo Results written to shares.txt
echo.

REM Disks
echo Getting disk info...
wmic diskdrive list brief > disks.txt
echo. >> disks.txt
wmic partition list brief >> disks.txt
echo. >> disks.txt
wmic logicaldisk get DeviceID,FreeSpace,ProviderName,Size,VolumeName,VolumeSerialNumber,Description,Filesystem /format:list >> disks.txt
echo Results written to disks.txt
echo.

REM Sysinfo
echo Getting system info...
wmic computersystem get Caption,DaylightInEffect,description,domain,enabledaylightsavingstime,manufacturer,model,name,numberofprocessors,partofdomain,primaryownercontact,primaryownername,roles,supportcontactdescription,systemstartupoptions,systemtype,totalphysicalmemory,username /format:list > systeminfo.txt
echo . >> systeminfo.txt
wmic os list full >> systeminfo.txt
echo Results written to systeminfo.txt
echo.

REM Patches
echo Getting installed patches...
wmic qfe where (NOT Description like '') get hotfixid,description,installedon,installedby /format:list > patches.txt
echo Results written to patches.txt
echo.

REM Installed software
REM This one takes a while, too, if you have lots of crap installed.
set choice=
set /p choice="Do you want to get installed software? This could take a while. Enter y or n: "
if '%choice%'=='n' goto finished
if '%choice%'=='y' goto getsw
echo.

:getsw
echo Getting installed software...
wmic product get name,installdate,packagecache,version,vendor /format:list > software.txt
echo Results written to software.txt
echo.

:finished
 echo Live Response complete.
 echo.
 
:end
