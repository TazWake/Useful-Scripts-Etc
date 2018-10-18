#
# This is incomplete - it is being used to store ideas and work towards a final goal
#

from scapy.all import *

packets = rdpcap('FILENAME.pcap')

counter = 0

# This version dumps the first 1000 packets out of a pcap in hex

for packet in packets:
    counter = counter + 1
    if counter =>0 and counter < 1001:
        hex_dump = ':'.join(x.encode('hex') for x in str(packet))
        print "### Packet : "+ str(counter)
        print hex_dump
        print "\n"
    if counter == 1001:
        break
