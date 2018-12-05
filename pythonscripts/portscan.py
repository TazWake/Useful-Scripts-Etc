import optparse
from socket import *
from threading import *
'''
This script attempts to validate if a port is listening on a target server. It does this by sending a small packet of data and checking for the response. If the server doesnt recognise the packet of data it may choose to ignore the request.
For HTTP/HTTPS servers, this is an effective test - however for other protocols it may result in false-closed replies.
'''
screenLock = Semaphore(value=1)

def connScan(tgtHost, tgtPort):
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))
        connSkt.send(b'Peek-a-boo\r\n')
        results = connSkt.recv(100)
        screenLock.acquire()
        results = results.decode()
        print('[+]%d/tcp open'% tgtPort)
        print('[+] ' + str(results))
    except:
        screenLock.acquire()
        print('[-]%d/tcp closed'% tgtPort)
    finally:
        screenLock.release()
        connSkt.close()

def portScan(tgtHost, tgtPorts):
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print("[-] Cannot resolve '%s': Unknown host"%tgtHost)
        return
    try:
        tgtName = gethostbyaddr(tgtIP)
        print('\n[+] Scan results for: ' + tgtName[0])
    except:
        print('\n[+] Scan results for: ' + tgtIP)
    setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        t = Thread(target=connScan, args=(tgtHost, int(tgtPort)))
        t.start()

def main():
    """
    This script scans a single host for identified ports.
    In its current version is works best as detecting web servers.
    """
    parser = optparse.OptionParser('usage%prog '+\
                                   '-H <target host> -p <target port>')
    parser.add_option('-H', dest='tgtHost', type='string', help='Specify target host')
    parser.add_option('-p', dest='tgtPort', type='string', help='Specify target port[s] separated by a comma.')
    (options, args) = parser.parse_args()
    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPort).split(',')
    if(tgtHost == None) | (tgtPorts[0] == None):
        print(parser.usage)
        exit(0)
    portScan(tgtHost, tgtPorts)
if __name__ == "__main__":
    main()
