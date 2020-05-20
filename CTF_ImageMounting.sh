#!/bin/bash

# ############################################
# Evidence mountscript
# Arguments:
#           1: path to EO1 file
# Assumptions:
#           Only one EO1 file is being mounted
# ############################################# 

echo "****************"
echo "* STARTING RUN *"
echo "****************"
ewfmount $1 /mnt/ewf/
echo "Image mounted to /mnt/ewf/"
mount -o ro,loop,show_sys_files,streams_interface=windows /mnt/ewf/ewf1 /mnt/windows_mount/
echo "Windows mount completed"
ls -alhF /mnt/windows_mount/
echo "****************"
echo "*  COMPLETED   *"
echo "****************"
