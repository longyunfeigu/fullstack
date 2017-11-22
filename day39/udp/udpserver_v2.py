#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
基于udp协议的服务端
"""
from socket import *

ip_port = ('127.0.0.1',8000)
phone = socket(AF_INET, SOCK_DGRAM)
phone.bind(ip_port)
# udp不需要建立连接，所以不需要listen监听链接
# udp不需要建立连接,自然也就没有链接循环和accept接入链接
while True:
    msg, client_addr = phone.recvfrom(1024)
    # client_addr是('127.0.0.1', 52528)
    print(msg, client_addr)
    phone.sendto(msg.upper(), client_addr)



