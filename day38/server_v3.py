#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
socket服务端
"""
import socket
import struct
import subprocess

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
            recv_cmd = conn.recv(1024)
            # linux情况下client终止连接，那么server的recv会收到空，不会阻塞，也发空，一直循环收空发空的操作，程序卡死在这循环中
            if not recv_cmd:
                break
            print('接收到客户发来的信息', recv_cmd)
            res = subprocess.Popen(recv_cmd.decode('utf-8'), shell=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # 这样写的bug在于linux系统ls;pwd;sdaa这样连接的多条命令的执行,解决办法是把错误结果和正确结果都发送过去
            # err = res.stderr.read()
            # if err:
            #     ret = err
            # else:
            #     ret = res.stdout.read()
            # conn.send(ret.encode('utf-8'))
            err = res.stdout.read()
            correct = res.stdout.read()
            err_length = len(err)
            correct_length = len(correct)
            err_correct_length = err_length + correct_length


            # 发送协议头,定制为固定长度的4个字节
            conn.send(struct.pack('i', err_correct_length))

            # 发送数据部分
            conn.send(err)
            conn.send(correct)

        except ConnectionResetError as e:
            break   # 退出循环表示client终止连接
    conn.close()
phone.close()
