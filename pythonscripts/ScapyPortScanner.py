#!/usr/bin/env python

import sys, logging, optparse
from scapy.all import *

'''Updated script to scan ports using scapy'''

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

def main():
    parser = optparse.OptionParser('usage%prog -i <IP> -p <Ports>')
    parser.add_option('-i', dest='ipaddr', type='string', help='Specify the IP address you want to scan')
    parser.add_option('-p', dest='dports', type='string', help='Specify the port you want to scan - indivdual or comma separated list')
    (options, args) = parser.parse_args()
    scan_dest = options.ipaddr
    scan_ports = options.dports
    if scan_ports == "":
        scan_ports = [21,22,80,139,443,445]
    packet=IP(dst=scan_dest,ttl=60)/TCP(dport=scanports,flags="S")
    responded, unanswered = sr(packet, timeout=10, verbose=0)
    print("List of all open ports in "+scan_dest)
    for x in responded:
        if x[1][1].flags==18:
            print x[1].sport

if __name__ == "__main__":
    main()
