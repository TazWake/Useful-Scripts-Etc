#!/usr/bin/env python3
# note - this script requires https://github.com/mhammond/pywin32
from __future__ import print_function
import pywintypes
import win32api
import win32con
import optparse

'''
This script scans a clean (new build) system and establishes a baseline of known good paths and service binaries.
Useage: python ServiceBaseline.py [options]
Options: -f <path and filename> | The path & filename you want the output saved
'''

def main():
    parser = optparse.OptionParser('useage%prog -f <path and filename>')
    parser.add_option('-f', dest='filename', type='string', help='Path and filename to where you want the output saved')
    (options, args) = parser.parse_args()
    f = options.filename
    read_perm = (win32con.KEY_READ | 
                 win32con.KEY_ENUMERATE_SUB_KEYS |
                 win32con.KEY_QUERY_VALUE)
    hkey = win32api.RegOpenKeyEx(win32con.HKEY_LOCAL_MACHINE,"SYSTEM\\ControlSet001\\Services",0,read_perm)
    names = [data[0] for data in win32api.RegEnumKeyEx(hkey)]
    for name in names:
        try:
            subkey = win32api.RegOpenKeyEx(hkey,"%s\\Parameters" % name,0, read_perm)
            value = win32api.RegQueryValueEx(subkey,"ServiceDLL")
        except pywintypes.error:
            continue
        path = win32api.ExpandEnvironmentStrings(value[0])
        name = name.lower()
        path = path.lower()
        print(name, " = ", path)
        f = open(f,wt)
        f.write(name, " = ", path)
        f.close

        
if __name__ == '__main__':
    main()
