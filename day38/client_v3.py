#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
v3版本的缺点是如果要发送的数据量很大,比如22222222222222222，struct模块pack的时候就会溢出
解决方法是发送一个json字典,字典里包含发送的内容的长度信息.这个灵感的来源是协议头不仅仅要包含长度信息,可能还会包含其他信息
"""
import socket
import struct
import sys
# 买一个手机
phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 直接打电话，客户端的SIM号无所谓不重要
phone.connect_ex(('127.0.0.1', 8000))

while True:   # 拨通电话后循环收发消息,循环不包括connect,包裹的仅仅是收发消息
    cmd = input('>>> ')
    # 这个判断的意义是如果为空，send不会阻塞，但是server端的recv会阻塞,所以client不允许发送空
    if not cmd:
        continue
    phone.send(cmd.encode('utf-8'))
    print('客户端信息已经发送')
    # 收固定长度的4个字节
    ret_length = struct.unpack('i', phone.recv(4))[0]

    # 循环接受数据
    ret = b''
    already_recv_length = 0
    while already_recv_length < ret_length:
        recv_data = phone.recv(1024)
        already_recv_length += len(recv_data)
        ret += recv_data
    print(ret.decode('gbk'))

phone.close()
