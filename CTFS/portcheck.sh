#!/bin/bash
echo "Quick scan of ports"
ports=$(nmap -p- --min-rate 1000 -T4 $1 | grep ^[0-9] | cut -d '/' -f 1 | tr '\n' ',' | sed s/,$//)  
echo "Open Ports identified"
echo "Scanning now"
nmap -Pn -sC -sV -vvvv --reason -oA AllTCP -p $ports $1
echo "Scanning complete"
