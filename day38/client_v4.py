#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
socket客户端
"""
import socket
import struct
import json
# 买一个手机
phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 直接打电话，客户端的SIM号无所谓不重要
phone.connect(('127.0.0.1', 8000))

while True:   # 拨通电话后循环收发消息,循环不包括connect,包裹的仅仅是收发消息
    cmd = input('>>> ')
    # 这个判断的意义是如果为空，send不会阻塞，但是server端的recv会阻塞,所以client不允许发送空
    if not cmd:
        continue
    phone.send(cmd.encode('utf-8'))
    print('客户端信息已经发送')
    # 收固定长度的4个字节
    headers_length = struct.unpack('i', phone.recv(4))[0]
    headers_str = phone.recv(headers_length)
    headers_dict = json.loads(headers_str)
    ret_length = headers_dict.get('data_length')
    # 循环接受数据
    ret = b''
    already_recv_length = 0
    while already_recv_length < ret_length:
        recv_data = phone.recv(1024)
        already_recv_length += len(recv_data)
        ret += recv_data
    print(ret.decode('gbk'))

phone.close()
