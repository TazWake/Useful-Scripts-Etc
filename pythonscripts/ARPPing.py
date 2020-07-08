#! /usr/bin/env python
import sys
import datetime
from scapy.all import srp,Ether,ARP,conf

x=datetime.datetime.now()
f=x.strftime("%X")

def scan(net):
    conf.verb=0
    ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=net),timeout=2)
    #filename="Scan_"+f+"_"+str(net)+".csv"
    filename="Scan_"+f+".csv"
    print("Scan results will be saved to:" + filename)
    q = open(filename,"w")
    print("MAC -- IP")
    q.write("MAC Address,IP Address\n")
    for snd,rcv in ans:
        print(rcv.sprintf(r"%Ether.src% -- %ARP.psrc%"))
        q.write(rcv.sprintf(r"%Ether.src%,%ARP.psrc%"))
        q.write("\n")
    q.close()
    return

def main():
    if len(sys.argv) != 2:
        print("Usage: ARPPing.py <net>\n Example: ARPPing.py 192.168.1.0/24")
        sys.exit(1)
    net=sys.argv[1]
    print("############################################################\n######## Beginning Scan at "+x.strftime("%c") + " ########\n############################################################\n")
    scan(net)
    print("\n################################\n######## Scan Completed ########\n################################")

if __name__ == "__main__":
    main()
