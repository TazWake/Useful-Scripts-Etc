#!/usr/bin/env python
import optparse
from scapy.all import *

'''
This is the script for Trophy 2
'''

def singleicmp(ipadd):
    '''Send a single ICMP packet to a specified IP address'''
    packet=IP(dst=ipadd,ttl=64)/ICMP()
    pingu = sr1(packet)
    return(pingu)

def icmpframe(ipadd):
    '''build an implicit ICMP frame (i.e. layer 2) with a TTL value from to 2 to 7 & send to the network etc'''
    # This is incomplete
    packet=IP(dst=ipadd,ttl=[2,7])/ICMP()
    pingu = sr1(packet)
    pingu.nsummary()
    return()

def foreverping(ipadd):
    '''send ICMP echo request forever using the sr*() function that send packets forever etc'''
    # not yet started

def sslsniff(tbc):
    '''This challenge involves sniffing 5 packets on port 443'''
    # not yet started

def main():
    parser = optparse.OptionParser('usage%prog -i <IP Address to ping>')
    parser.add_option('-i', dest='ipadd', type='string', help='The IP address you want to ping')
    (options, args) = parser.parse_args()
    ipadd = options.ipadd
    a = singleicmp(ipadd)
    print("\n-------ICMP ping sent----------\n")
    print("-------The reply is:-----------\n")
    a.show()
    print("\n-------------------------------\n")
    # This script may be having problems #
    

if __name__ == "__main__":
    main()
