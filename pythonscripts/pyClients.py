import socket
"""
This is for quick tcp/udp connections, with the idea being that they can be copypasta'd into other scripts.

Eventually this will be turned into a standalone client connect script
"""
def tcpConnect(host,port,data):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host,post))
    client.send(data)
    response = client.recv(4096)
    print response
    return response

def udpConnect(host,port,data):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto(data,(host,port))
    resp,addr = client.recvfrom(4096)
    print resp
    return resp

def main():
    # Define defaults
    data = "GET / HTTP/1.1\r\nHhost: "+host+"\r\n\r\n"
