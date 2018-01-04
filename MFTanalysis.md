# Master File Table Analysis
This document will be used to capture some methods for identifying, extracting and confirming the presence of files on a captured image.
Although not perfect, this can provide assistance in detecting anti-forensics methods. However, be aware that no one approach is perfect and multiple methods may be required.

## Checking MFT for malware 
In this example, we are believe the attackers used `scvhost.exe` as their payload and know it was installed under a temp folder in C:\Windows. We are going to use the [SIFT](https://digital-forensics.sans.org/community/downloads) command line to check our theory.

```ls -li /mnt/windows_mount/Windows/TEMP/scvhost.exe```

This will confirm the presence of the file and return an `inode` (the first number). For example you will get something like this:
```62164 -rwxrwxrwx 1 root root 102400 Mar 31  2003 /mnt/windows_mount/Windows/TEMP/scvhost.exe```
You can use `istat` to pull additional information such as the $SI and $FN timestamps using the inode number (in this example it is **62164**)

```istat {path/to/disk/image}.E01 62164```

The output should look like something like this:
```
$STANDARD_INFORMATION Attribute Values:
Flags: Archive
Owner ID: 0
Security ID: 1686  (S-1-5-21-2036804247-3058324640-2116585241-1673)
Last User Journal Update Sequence Number: 1915501416
Created:	2003-03-31 14:00:00.000000000 (UTC)
File Modified:	2003-03-31 02:12:36.000000000 (UTC)
MFT Modified:	2017-04-02 02:22:00.171508200 (UTC)
Accessed:	2017-04-01 23:40:19.003151200 (UTC)

$FILE_NAME Attribute Values:
Flags: Archive
Name: svchost.exe
Parent MFT Entry: 380 	Sequence: 26
Allocated Size: 102400   	Actual Size: 102400
Created:	2017-04-01 08:40:24.143281400 (UTC)
File Modified:	2017-04-01 22:40:25.413910900 (UTC)
MFT Modified:	2017-04-01 23:35:55.958743200 (UTC)
Accessed:	2017-04-01 23:40:19.003151200 (UTC)
```
Looking at this, there is strong evidence that this file has been [timestomped](http://www.forensicswiki.org/wiki/Timestomp) and in most cases this would be evidence of malicious activity.



