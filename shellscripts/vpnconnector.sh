#!/bin/bash

if [ $# -ne 1 ]
    then
        echo "Usage: .\vpnconnector.sh <path>"
        exit
fi

FILES_ARRAY=(`ls -a $1`)
FILES_ARRAY_LENGTH=${#FILES_ARRAY[@]}

return_random() {
    candidate=$((RANDOM % $FILES_ARRAY_LENGTH))
    choice=${FILES_ARRAY[candidate]}
}

return_random

while [ $choice = "." -o $choice = ".." ]
    do
        return_random
    done

echo "Trying: \"$choice\", $candidate of $FILES_ARRAY_LENGTH in $1"
`openvpn $1/$choice`
