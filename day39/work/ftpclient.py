#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import struct
import json
import os


def auth(func):
    def inner(self):
        while True:
            print(self.socket.recv(1024).decode('utf-8'))
            username = input('>>>:').strip()
            self.socket.sendall(username.encode('utf-8'))
            print(self.socket.recv(1024).decode('utf-8'))
            password = input('>>>:').strip()
            self.socket.sendall(password.encode('utf-8'))
            confirm_msg = self.socket.recv(1024)
            if confirm_msg == b'yes':
                print('登录成功')
                msg = func(self)
                break
                return msg
    return inner



class FTPClient:
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    max_package_size = 8192
    coding = 'utf-8'
    client_dir = 'C:\\Users\Administrator\\PycharmProjects\\fullstack'

    def __init__(self, server_address, connect=True):
        """Constructor.  May be extended, do not override."""
        self.server_address = server_address
        self.connect = connect
        self.socket = socket.socket(self.address_family, self.socket_type)

        if connect:
            try:
                self.client_connect()
            except:
                self.client_close()
                raise

    def client_connect(self):
        """Called by constructor to bind the socket.

           May be overridden.
        """
        self.socket.connect_ex(self.server_address)

    def client_close(self):
        """Called to clean-up the server.
        May be overridden.
        """
        self.socket.close()

    @auth
    def run(self):
        """merely processing client command"""
        if not self.connect:
            self.client_connect()
        while True:    # 通信循环
            cmd = input('>>>:').strip()
            if not cmd:
                continue
            cmd_list = cmd.split(' ')
            command = cmd_list[0]
            if hasattr(self, command):
                func = getattr(self, command)
                func(cmd_list)
            elif cmd.startswith('ls'):
                pass

            else:
                print('命令格式输入有误')



    def put(self, args):
        # 规范化文件路径，os.path.normpath在linux平台无效
        file_path = os.path.normpath(args[-1])
        if not os.path.exists(file_path):
            print('要上传的文件不存在')
            # 此处调用return是为了防止else语句块过大
            return
        else:
            file_size = os.stat(file_path).st_size
        # 发送头信息
        headers_dict = {'command': args[0], 'filename': os.path.basename(file_path), 'filesize': file_size}
        headers_json = json.dumps(headers_dict)
        headers_bytes = headers_json.encode(self.coding)
        # 注意，struct发的是长度，先把头的长度再发过去，然后在send头信息，server取固定的头长度得到头信息长度，根据
        # 头长度取得头信息，因此这里的两次send不会粘包，因为有头信息来控制
        self.socket.send(struct.pack('i', len(headers_bytes)))
        self.socket.send(headers_bytes)

        send_size = 0
        with open(file_path, 'rb') as f:
            for line in f:
                already_send_size = len(line)
                self.socket.send(line)
                send_size += already_send_size
                # print(send_size)
            else:
                print('upload success')

    def get(self, args):
        headers_dict = {'command': args[0], 'filename': args[-1]}
        headers_json = json.dumps(headers_dict)
        headers_bytes = headers_json.encode(self.coding)
        headers_length = len(headers_bytes)
        self.socket.send(struct.pack('i', headers_length))
        self.socket.send(headers_bytes)

        headers_struct = self.socket.recv(4)
        headers_length = struct.unpack('i', headers_struct)[0]
        headers_str = self.socket.recv(headers_length)
        headers_dict = json.loads(headers_str)
        err_msg = headers_dict.get('err_msg', None)
        if err_msg:
            print(err_msg)
            return
        file_path = os.path.join(self.client_dir, args[-1])
        print(file_path)
        filesize = headers_dict.get('file_size')
        already_recv_size = 0
        with open(file_path, 'wb') as f:
            while already_recv_size < filesize:
                recv_data = self.socket.recv(self.max_package_size)
                f.write(recv_data)
                already_recv_size += len(recv_data)

if __name__ == '__main__':
    obj = FTPClient(('127.0.0.1', 13140))
    obj.run()



