#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
基于udp的socket因为不需要建立连接，所以不需要先启动服务端再启动客户端，先启动哪一端都不会报错
基于udp协议的客户端
"""
from socket import *

ip_port = ('127.0.0.1',8000)
phone = socket(AF_INET, SOCK_DGRAM)
# udp不需要建立连接，所以不需要connect

while True:
    msg = input('>>>').strip()
    phone.sendto(msg.encode('utf-8'), ip_port)
    # server_addr是('127.0.0.1', 8000)
    msg, server_addr = phone.recvfrom(1024)
    print(msg, server_addr)



