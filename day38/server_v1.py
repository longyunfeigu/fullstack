#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
socket服务端
"""
import socket
# 买一个手机
phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# closesocket（一般不会立即关闭而经历TIME_WAIT的过程）后想继续重用该socket
phone.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# 绑定SIM卡
phone.bind(('127.0.0.1', 8000))

# 最多可以接进来几个电话，一个电话结束可以迅速切换到另一个电话(事先建立好的连接池)
phone.listen(5)
print('starting...')

conn, addr = phone.accept()


data1 = conn.recv(1014)

# data2 既然收到的内容为空也就是收不到内容为什么不会阻塞呢？
# 因为客户端程序已经正常执行完毕了,区别于之前的client发空然后recv的情况
data2 = conn.recv(1024)

print(data1)
print(data2)

