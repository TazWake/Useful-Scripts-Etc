# Timeline Creation
This is basic guide on some common steps to create timelines / super timelines.
It may not be applicable to every situation and you should adapt this to your preferences, tools and investigative requirements.

This assumes you have a disk image in E01 format and a memory image collected from the same machine.

## Mount the evidence file
```shell
ewfmount {path/to/file}.E01 /mnt/ewf_mount
cd /mnt/ewf_mount
mount -o ro,loop,show_sys_files,streams_interface+windows ewf1 /mnt/windows_mount
```

## Extract filesystem bodyfile from evidence file
```fls -r -m C: {path/to/file}.E01 > {path/to/file}-bodyfile```

## Volatility Timeliner
```vol.py -f {path/to/file}.raw --profile=PROFILE timeliner --output=body --outputfile={path/to/file}/timeliner.body```

## Combine timelines
```cat {path/to/file}/timeliner.body >> {path/to/file}-bodyfile```

## Extract the combined timeline
```mactime -d -b {path/to/file}-bodyfile {start date}..{end date} > {path/to/file}-mactime-timeline.csv```

## Keyword Whitelist
If there is a keyword whitelist, this can be used to filter against.
```grep -v -i -f {path/to/file}whitelist.txt {path/to/file}-mactime-timeline.csv > {path/to/file}-mactime-timeline-final.csv```

## Supplementary Data Collection
### RegRipper to verify data
```shell
cd /mnt/windows_mount/users/{USERNAME}
rip.pl -r NTUSER.DAT -p recentdocs > {path/to/file}/recent-docs.txt
cat {path/to/file}/recent-docs.txt
```
### RegRipper to check wordwheel query
```shell
cd /mnt/windows_mount/users/{USERNAME}
rip.pl -r NTUSER.DAT -p wordwheelquery > {path/to/file}/wordwheelquery.txt
cat {path/to/file}/wordwheelquery.txt
```
### Carving Prefetch
#### using pf (licence required)
```shell
pf -v /mnt/windows_mount/Windows/Prefetch/{prefetchfile}.pf
```

# Super Timeline Creation

## Mount the evidence file
```shell
ewfmount {path/to/file}.E01 /mnt/ewf_mount
cd /mnt/ewf_mount
mount -o ro,loop,show_sys_files,streams_interface+windows ewf1 /mnt/windows_mount
```

## Gather timeline data
```log2timeline.py {path/to/file}plaso.dump {path/to/file}.E0```

## Filter
```psort.py -z "UCT" -o L2tcsv {path/to/file}plaso.dump "date > '{start date}' AND date < 'end date'" > {path/to/file}plaso.csv```
Note: The dates should be in YYYY-MM-DD HH:MM:SS format. For example: `2018-01-01 00:00:01`.

## Keyword whitelist
```grep -v -i -f {path/to/file}whitelist.txt {path/to/file}plaso.csv > supertimeline.csv```


