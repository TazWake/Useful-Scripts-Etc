#!/bin/bash

# This script logs all file deletion requests

removelog="/var/log/remove.log"

# Tests user input, generating a simple file listing if no arguments are given
if [ $# -eq 0 ] ; then
    echo "Usage: $0 list of files or directories" >&2
    exit 1
fi

# Records the user action to the logfile
echo "$(date): ${USER}: $@" >> $removelog

# Passes the request to the real rm program
/bin/rm "$@

exit 0
