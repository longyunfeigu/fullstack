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
# 有一点需要注意：msg输入空，server端不会recv_from不会阻塞
# 原因是udp是基于包的，每个包都有头，所以一方面不存在粘包，另一方面发的消息数据部分为空，但是数据包还有头信息，所以
# 整个数据包并非为空，所以recv_from不会阻塞
msg = input('>>>')
phone.sendto(msg.encode('utf-8'), ip_port)
# server_addr是('127.0.0.1', 8000)
msg, server_addr = phone.recvfrom(1024)
print(msg, server_addr)



