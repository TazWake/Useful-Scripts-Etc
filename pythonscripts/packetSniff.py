import socket
import struct
import codecs
import itertools

protocols = {17:'UDP', 6:'TCP', 1:'ICMP'}

#Special code for all Ethernet protocols (not protocol 3)
#Complete list of possible values is here: http://lxr.free-electrons.com/source/include/linux/if_ether.h?v=2.6.24
s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
#All IP protocols
#s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0800))
#The next two lines are required for windows, not linux
#s.bind(("192.168.127.128",0))
#s.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)

def tcp_flags_as_str(flag):
    file_flags = ['CWR',  'ECE', 'URG', 'ACK', 'PSH', 'RST', 'SYN', 'FIN']
    return "|".join(list(itertools.compress(file_flags,map(int,format(flag,"08b")))))
while True:
    data,metax = s.recvfrom(65535)
    (eth_src,eth_dst,eth_type) = struct.unpack('!6s6sH' , data[:14])
    if hex(eth_type) == "0x806":
        print("ARP: SRC:{0} DST:{1}".format(codecs.encode( eth_src,"hex"), codecs.encode(eth_dst,"hex")))
        continue
    elif hex(eth_type) != "0x800":
        #If the embeded Ethernet protocol is not 0x800 (IP Protocol), Alert and skip it
        print("WARNING - SKIPPING A NON IP PACKET. TYPE:{0}".format((hex(eth_type))))
        continue
    print("ETH: SRC:{0} DST:{1} TYPE:{2}".format(codecs.encode(eth_src,"hex"), codecs.encode( eth_dst,"hex"), hex(eth_type)))
    #Now lets unpack the IP Header.  Ethernet header is 14 bytes long and IP header (without options) is 20
    (ip_byte0, ip_svc, ip_total_len,ip_id,ip_frag,ip_ttl,ip_proto,ip_chksum,ip_src,ip_dst) = struct.unpack('!BBHHHBBHLL',data[14:34])
    ip_version = ip_byte0>>4
    ip_header_length = (ip_byte0 & 15)  * 4
    srcip = socket.inet_ntoa(struct.pack('!L',ip_src))
    dstip = socket.inet_ntoa(struct.pack('!L',ip_dst))
    #Now see it it has options and calculate length on 4 byte boundaries
    ip_options_length =  (( ip_header_length-20 + 3 ) // 4) *4
    #unpack all the ip opions into a string of length ip_options_length 
    structstring = "!{0}s".format(ip_options_length)
    ip_options = struct.unpack(structstring, data[34:34+ip_options_length])
    embeded_protocol = protocols.get(ip_proto, str(ip_proto))
    print("IP: SRC:{0} DST:{1} - {2} ".format(srcip, dstip, embeded_protocol))
    embeded_data = data[34+ip_options_length:]
    if embeded_protocol == "TCP":
        (tcp_sport,tcp_dport,tcp_seq,tcp_ack,tcp_hlen,tcp_flag,tcp_window,tcp_chksum,tcp_urg) = struct.unpack('!HHIIBBHHH',embeded_data[:20])
        tcp_header_length=(tcp_hlen>>4)*4
        tcp_data_length=ip_total_len-(20+ip_options_length+tcp_header_length)
        tcp_data = embeded_data[tcp_header_length:]
        print("  +TCP: SPORT: {0} DPORT: {1} Flags: {2}".format(tcp_sport,tcp_dport,tcp_flags_as_str(tcp_flag)))
        print("      +-Data: {0} ".format(codecs.encode(data,"HEX")))
        print("      +-Text: {0} ".format(tcp_data))
    elif embeded_protocol == "UDP":
        (udp_sport, udp_dport, udp_len, udp_chksum) = struct.unpack('!HHHH',embeded_data[:8])
        print("  +UDP: SPORT:{0} DPORT:{1} LEN:{2} CHKSUM:{3} ".format(udp_sport, udp_dport, udp_len, udp_chksum))
        print("     +-Data: {0} ".format(codecs.encode( embeded_data[8:],"HEX")))
        print("     +-Text: {0} ".format(embeded_data[8:]))
    elif embeded_protocol =="ICMP":
        #ICMP Header = Type 1 byte, Code 1 byte, checksum 2 bytes, data 4 bytes
        (icmp_type,icmp_code,icmp_chksum,icmp_data) = struct.unpack(r'!BBHI',embeded_data[:8])
        if icmp_type==0:
            print("ICMP - PING REPLY SRC:{0} DST:{1}".format(srcip, dstip))
        elif icmp_type==3:
            print("ICMP - UNDELIVERABLE SRC:{0} DST:{1} CODE:{2}".format(srcip, dstip, icmp_code))
        elif icmp_type==8: 
            print("ICMP - PING REQUEST SRC:{0} DST:{1}".format(srcip, dstip))
    else:
        print("*"*1000)
        print("WARNING: AN UNHANDLED PROTOCOL WAS DISCOVERED - PROTOCOL NUMBER ", embeded_protocol)
        print("Data: " + codecs.encode(data,"hex").decode())
        print("*"*1000)
