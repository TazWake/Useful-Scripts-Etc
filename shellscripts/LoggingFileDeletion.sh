#!/bin/bash

# This script logs all file deletion requests
# Usage
# -----
# Option 1
# Save the script as a local file - eg: logrm.sh
# alias rm=logrm
#
# Option 2
# rename /bin/rm to /bin/rm.old (change line 27 to match this)
# save this file as /bin/rm


removelog="/var/log/remove.log"

# Tests user input, generating a simple file listing if no arguments are given
if [ $# -eq 0 ] ; then
    echo "Usage: $0 list of files or directories" >&2
    exit 1
fi

# Records the user action to the logfile
echo "$(date): ${USER}: $@" >> $removelog

# Passes the request to the real rm program - note if you have renamed it (option 2 above) you must change this line
/bin/rm "$@

exit 0
