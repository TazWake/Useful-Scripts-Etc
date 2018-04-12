#!/bin/bash
nmap -sT 192.168.1.0/24 -p 21 -oG ftp
cat ftp | grep open > ftp_open
cat ftp_open | cut -f2 -d";" | cut -f1 -d"(" > ftp_open_cut
for name in $(cat ftp_open_cut); do
    nmap -sV -p 21 $name > ftp_name.txt
done
