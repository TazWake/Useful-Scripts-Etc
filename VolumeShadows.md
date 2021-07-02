# Analysing Volume Shadows

This is a quick guide for interacting with Windows volume shadow copies using [SIFT](https://digital-forensics.sans.org/community/downloads)

*Note: You need to use uncompressed images for this. If you have E01 or similar, they have to be converted before use

## Use ewfmount to create raw image
This assumes the file you are analysing is in E01 format.
```shell
ewfmount {path/filename}.E01 /mnt/ewf_mount
```
*Note: if you are investigating multiple systems you may need to use different mount points.*

## View available shadows
Next check to see what shadows are available in the image
```shell
vshadowinfo /mnt/ewf_mount/ewf1
```
*Note: the path should reflect the path used above*

Look at the data provided and make a note of which, if any, shadow copy is of special interest.

## Use vshadowmount to make raw images of shadows
```shell
vshadowmount /mnt/ewf_mount2/ewf1 /mnt/vss
```
This will create a file for each available volume shadow copy

## Mount one or many shadow volumes
If you have a specific volume you are interested in, mount that otherwise consider mount all.

### Mount a single shadow volume
```shell
mount -o ro,loop,show_sys_files,streams_interface=windows /mnt/vss/vss4 /mnt/shadow_mount/vss4
```

### Or mount all volume shadows at the same time:
```shell
cd /mnt/vss
for file in *; do
    mount -o ro,loop,show_sys_files,streams_interface=windows /mnt/vss/$file /mnt/shadow_mount/$file
done
```

## Analysis examples
### Compare the same file across multiple volumes:
```shell
cd /mnt/shadow_mount
ls -l */Windows/AppCompat/Programs/RecentFileCache.bcf
```

## Unmount everything when done:
```shell
cd /mnt/shadow_mount
for file in *; do umount $file; done
umount /mnt/vss
umount /mnt/ewf_mount
```
