#!/bin/bash
echo "Assessment underway"

# This script is a place holder for various checks
# it is expected to grow and develop depending on requirements
# it is not a default DFIR script

HOST_NAME = $(hostname)
FILE = "/etc/shadow"
REMOTE = "www.google.com"

echo "Script is running on ${HOST_NAME}."
if[ -e "$FILE"]
then
    echo "Shadow passwords are enabled on this system."
fi

if [ -w "$FILE"]
then
    echo "This account has permission to edit ${FILE}."
else
    echo "This account does NOT have permission to edit ${FILE}."
fi

ping -c 1 $HOST
if[ "$?" -eq "0"]
then
    echo "$HOST is reachable."
else
    echo "$HOST is not reachable."
fi
