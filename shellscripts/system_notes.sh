#!/bin/bash
echo "Assessment underway"

# This script is a place holder for various checks
# it is expected to grow and develop depending on requirements
# it is not a default DFIR script

HOST_NAME = $(hostname)
FILE = "/etc/shadow"

echo "Script is running on ${HOST_NAME}."
if[ -e "$FILE"]
then
    echo "Shadow passwords are enabled on this system."
fi
