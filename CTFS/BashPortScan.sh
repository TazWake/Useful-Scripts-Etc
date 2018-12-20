#!/bin/bash
#created by TMFS24 not me
#24-07-2018

echo "Checks for open tcp ports on host"

if [ "$#" -ne 1 ]; then
	echo "Usage $0 x.x.x.x"
	exit 1
fi
port=1
while [ $port -le 65535 ]
do
	(echo > /dev/tcp/$1/$port) > /dev/null 2>&1 
	if [ $? -eq 0 ]; then
	       	echo "$port is open"
	fi 

	if [ $((port % 1000)) -eq 0 ]; then
		echo "Ports upto $port scanned"
	fi
	port=$((port+1))
done
echo "Scan complete for $1"
