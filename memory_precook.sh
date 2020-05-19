#!/bin/bash

# This script runs a standard battery of memory analysis tools against a sample image to provide a standardised set of artefacts
# Two arguments are required - the file name of the memory image and the volatility profile to be used
# With volatility 3, the second argument can be removed and the script modified appropriately
 
echo "********************"
echo "Extracting Volatility Data"
# This is the basic run of commands with each plugin storing data to a text file.
vol.py -f $1 --profile=$2 pslist --output-file=pslist.txt
vol.py -f $1 --profile=$2 psscan --output-file=psscan.txt
vol.py -f $1 --profile=$2 pstree --output-file=pstree.txt
vol.py -f $1 --profile=$2 psxview --output-file=psxview.txt
vol.py -f $1 --profile=$2 netscan --output-file=netscan.txt
vol.py -f $1 --profile=$2 cmdscan --output-file=cmdscan.txt
vol.py -f $1 --profile=$2 consoles --output-file=consoles.txt
vol.py -f $1 --profile=$2 hivelist --output-file=hives.txt
vol.py -f $1 --profile=$2 prefetchparser --output-file=prefetchparser.txt
vol.py -f $1 --profile=$2 envars --output-file=envars.txt
vol.py -f $1 --profile=$2 dlllist --output-file=dlllist.txt
vol.py -f $1 --profile=$2 filescan --output-file=filescan.txt
vol.py -f $1 --profile=$2 shimcache --output-file=shimcache.txt
vol.py -f $1 --profile=$2 shimcachemem --output-file=shimcachemem.txt
vol.py -f $1 --profile=$2 getservicesids --output-file=serviceSIDS.txt
vol.py -f $1 --profile=$2 mimikatz --output-file=mimikatz.txt
mkdir malfind
vol.py -f $1 --profile=$2 malfind -D ./malfind/ --output-file=malfind.txt
mkdir MFT
vol.py -f $1 --profile=$2 mftparser -D ./MFT/ --output-file=mft.txt
echo "*** carving network data ***"
# This is to create two easier to read text files showing established and listening connections
head -n1 netscan.txt > established.txt
grep ESTABLISHED netscan.txt >> established.txt
head -n1 netscan.txt > listening.txt
grep LISTENING >> listening.txt
echo "*** network data carved ***"
echo "*** attempting hashdump ***"
# This will attempt to locate the SYSTEM and SAM hives and use them to dump hashes from the memory image.
syshive=$(grep SYSTEM hives.txt | cut -d" " -f1)
samhive=$(grep SAM hives.txt | cut -d" " -f1)
vol.py -f $1 --profile=$2 hashdump -y $syshive -s $samhive --output-file=hashdump.txt
# Password hashes should be in a crackable format now if required.
echo "Volatility Extraction Completed"
echo "********************"
echo ""
echo "********************"
echo "Running Bulk Extractor"
echo "********************"
mkdir bulk_output
bulk_extractor $1 -o ./bulk_output
echo "********************"
echo ""
echo "********************"
echo "*** Running Strings ***"
# as a final catch all strings are run against the image
strings -n 8 $1 > strings8.txt
strings -n 12 $1 > strings12.txt
echo "********************"
echo "Initial Assessment Completed"
echo "********************" 
