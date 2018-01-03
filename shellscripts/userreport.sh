#!/bin/bash
# This is a quick script to gather some key data on a system. It is not a forensic script.
# More entries will be added over time.

echo "Data Collection Report for $USER"
echo "================================"

echo "screen resolution"
echo xdpyinfo | grep dimensions

echo "Network Config written to file"
ifconfig > ./ifconfig.txt

echo "OS version"
uname -a

echo "Public IP"
curl icanhazip.com

echo "Generating Process List"
ps -al > ./pslist.txt

echo "================================"
