#!/bin/bash 
if ! printf '%s' "$1" | egrep -qi '^[-._a-z0-9]+:[0-9]+$' ; then  
    echo "uses openssl s_client to connect and dumps output to file (unless file exists)" echo "usage: $0 <host>:<port>" 1>&2 
    exit 1  
fi 
if[-e"$1"];then  
    echo "$1 skipping, file exists" 1>&2  
    exit 1 
fi  
echo "$1 connecting..." 1>&2 
sleep 10 | openssl s_client -connect "$1" > "$1" 2>&1 echo "$1 done." 1>&2  
