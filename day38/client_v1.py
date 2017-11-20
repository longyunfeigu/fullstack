#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
socket客户端粘包
"""
import socket

# 买一个手机
phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 直接打电话，客户端的SIM号无所谓不重要
phone.connect(('127.0.0.1', 8000))

phone.send(b'hello')
# 既然时间间隔短才结合在一起发送,那么我们就可以把间隔时间调长一点
import time
time.sleep(2)

phone.send(b'world')

phone.close()