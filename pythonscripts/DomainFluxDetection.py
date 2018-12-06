#!/usr/bin/env python
'''
This script is designed to help detect domain flux traffic.

The -f switch specifies the filename of the PCAP to be analysed.

Example: python DomainFluxDetection.py -f ExampleConficker.pcap
'''

from scapy.all import *
import optparse

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
    parser = optparse.OptionParser('usage%prog -f <pcap filename>')
    parser.add_option('-f', dest='pcapFilename', type='string', help='Specify the PCAP filename you want to examine')
    (options,args) = parser.parse.args()
    unAnsReqs = 0
    pcapf = options.pcapFilename
    if(pcapf == none):
        print(parse.usage)
        sys.exit()
    pkts = rdpcap(pcapf)
    for pkt in pkts:
        if DnsQuestion(pkt):
            unAnsReqs = unAnsReqs +1
    print("[!] " + str(UnAnsReqs)+ " unanswered name requests in total")

if __name__ == '__main__':
    main()
