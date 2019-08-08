#!/usr/bin/env python
import sys, logging, optparse
from scapy.all import *

'''Updated script to scan ports using scapy'''

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

def main():
    '''In this version, the ports scanned are hardcoded, future versions will allow users to specify'''
    parser = optparse.OptionParser('usage%prog -i <IP>')
    parser.add_option('-i', dest='ipaddr', type='string', help='Specify the IP address you want to scan')
    parser.add_option('-p', dest='dports', type='string', help='Specify the port(s) you want to scan')
    (options, args) = parser.parse_args()
    scan_dest = options.ipaddr
    scan_ports = options.dports
    # if scan_ports == None: # currently unused.
    #     scan_ports = [21,22,80,139,443,445] #currently unused.
    print("Checking for responses on ports [21,22,80,139,443,445]\n")
    packet=IP(dst=scan_dest,ttl=60)/TCP(dport=[21,22,80,139,443,445],flags="S")
    responded, unanswered = sr(packet, timeout=4, verbose=0)
    openprt = 0
    for x in responded:
        if x[1][1].flags==18:
            print(x[1].sport + " appears to be open")
            openprt = 1
    if openprt == 0:
        print("No open ports")

if __name__ == "__main__":
    main()
