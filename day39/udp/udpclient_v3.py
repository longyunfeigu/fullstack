from socket import *
# ip_port=('127.0.0.1',9003)
ip_port=('10.20.1.50',9003)
udp_client=socket(AF_INET,SOCK_DGRAM)

udp_client.sendto(b'hello', ip_port)
udp_client.sendto(b'world', ip_port)
