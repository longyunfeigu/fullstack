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

while True:    # 一直监听连接
    conn, addr = phone.accept()
    print('电话线是', conn)
    print('电话的另一头是', addr)

    while True:    # 循环收发消息
        try:    # windows情况下client终止连接会触发异常，因为连接断开的话conn就变成了一个损坏的连接
            recv_data = conn.recv(1024)
            # linux情况下client终止连接，那么server的recv会收到空，不会阻塞，也发空，一直循环收空发空的操作，程序卡死在这循环中
            if not recv_data:
                break
            print('接收到客户发来的信息', recv_data)
            conn.send(recv_data.upper())
        except ConnectionResetError as e:
            break   # 退出循环表示client终止连接
    conn.close()
phone.close()
