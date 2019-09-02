#!/usr/bin/env python
import optparse
from scapy.all import *

'''
Usage: python dnsquery.py [options]
Options: -n <IP> | The DNS server to be queried
         -l <domain name> | the domain name to look up
Example: python dnsquery.py -n 8.8.8.8 -l bbc.co.uk
'''


def dnsquery(nameserver, lookupname):
    query = IP(dst=nameserver, ttl=30)/UDP(sport=RandShort(), dport=53)/DNS(rd=1, qd=DNSQR(qname=lookupname, qtype="A"))
    answer = sr1(query)
    result = answer.an.rdata
    print("\n\nThe DNS A Record for " + nameserver + " is " + result)
    print("\nThe source address for this was: " + query.sprintf("%src%") + ":" + query.sprintf("%sport%"))
    return(result)


def multiples(nameserver, lookupname):
    implicitquery = IP(dst=nameserver, ttl=[61, 62, 63, 64, 65])/UDP(sport=RandShort(), dport=53)/DNS(rd=1, qd=DNSQR(qname=lookupname, qtype="A"))
    for pkt in implicitquery:
        answer = sr1(pkt)
        result = answer.an.rdata
        print("\nThis request has a TTL of: " + pkt.sprintf("%ttl%"))
        print("\nThe DNS A Record for " + nameserver + " is " + result)


def main():
    parser = optparse.OptionParser('usage%prog -n <DNS IP> -l <domain name to lookup>')
    parser.add_option('-n', dest='nameserver', type='string', help='Specify the nameserver to query')
    parser.add_option('-l', dest='lookupname', type='string', help='Specify the domain name to look up')
    (options, args) = parser.parse_args()
    a = options.nameserver
    b = options.lookupname
    answers = dnsquery(a, b)
    print("\nSending packets with varying TTL\n")
    answers = multiples(a, b)

if __name__ == "__main__":
    main()
