#!/usr/bin/env python
'''
This script is designed to help detect domain flux traffic.

Initial version requires the pcap to be called example.pcap. Options to be added later.
'''
from scapy.all import *
def DnsQuestion(pkt):
    if pkt.haslayer(DNSRR) and pkt.getlayer(UDP).sport == 53:
        rcode = pkt.getlayer(DNS).rcode
        qname = pkt.getlayer(DNS).qname
        if rcode == 3:
            print("[!] Name lookup failed: " + qname)
            return True
        else:
            return False
def main():
    unAnsReqs = 0
    pkts = rdpcap('example.pcap')
    for pkt in pkts:
        if DnsQuestion(pkt):
            unAnsReqs = unAnsReqs +1
    print("[!] " + str(UnAnsReqs)+ " unanswered name requests in total")
if __name__ = '__main__':
    main()
