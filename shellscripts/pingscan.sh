#!/bin/sh
#TMFS24 (Should be POSIX compliant)

echo "Pings hosts in final octet of IP Range"

if [ "$#" -ne 1 ]; then
	echo "Usage $0 x.x.x."
	exit 1
fi

i=1
while [ $i -le 254 ]
do
	( ping -c1 $1$i > /dev/null 2>&1;if [ $? -eq 0 ]; then echo "$1$i is up"; fi ) &
	
	i=$((i+1))
done

echo "Ping sweep complete!"
