#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
基于socketserver的ftpserver
"""
import struct
import json
import os
import socketserver
import random
import hmac

# class FTPServer(socketserver.BaseRequestHandler):
#     max_package_size = 8192
#     coding = 'utf-8'
#     allow_reuse_address = False
#     server_dir = '/tmp/upload'
#
#     def handle(self):
#         """merely processing service"""
#         while True:    # 通信循环
#             try:
#                 headers_struct = self.request.recv(4)
#                 if not headers_struct:
#                     break
#                 headers_length = struct.unpack('i', headers_struct)[0]
#                 headers_json = self.request.recv(headers_length)
#                 headers_dict = json.loads(headers_json)
#                 command = headers_dict.get('command')
#                 if hasattr(self, command):
#                     func = getattr(self, command)
#                     func(headers_dict)
#             except Exception as e:
#                 break
#
#     def put(self, args):
#         filename = args.get('filename')
#         filesize = args.get('filesize')
#         file_path = os.path.join(self.server_dir, filename)
#         already_recv_size = 0
#         with open(file_path, 'wb') as f:
#             while already_recv_size < filesize:
#                 recv_data = self.request.recv(self.max_package_size)
#                 f.write(recv_data)
#                 already_recv_size += len(recv_data)
#             else:
#                 print('download success')
#     def get(self, args):
#         print('getting.....')
#         filename = args.get('filename')
#         filepath = os.path.join(self.server_dir, filename)
#         if not os.path.exists(filepath):
#             err_msg = '服务器没有该文件'
#             headers_dict = {'err_msg': err_msg}
#         else:
#             filesize = os.path.getsize(filepath)
#             headers_dict = {'file_size': filesize}
#         # 发送数据之前先发数据的头信息
#         headers_str = json.dumps(headers_dict)
#         headers_bytes = headers_str.encode(self.coding)
#         headers_length = len(headers_bytes)
#         self.request.send(struct.pack('i', headers_length))
#         self.request.send(headers_bytes)
#
#         send_size = 0
#         with open(filepath, 'rb') as f:
#             print('write.....')
#             for line in f:
#                 already_send_size = len(line)
#                 self.request.send(line)
#                 send_size += already_send_size
#                 # print(send_size)

class FTPServer(socketserver.BaseRequestHandler):
    def handle(self):
        print(self.request)
        # self.request.send(''.encode('utf-8'))

def get_random_str(num):
    """
    得到随机字符串，用于后续加密
    :param num: 随机字符串位数
    :return: 随机字符串
    """
    str_list = []

    for i in range(num):
        j = random.randrange(num)
        if i == j:
            str_list.append(str(i))
        else:
            str_list.append(chr(random.randrange(97, 122)))
    # 打乱str_list里面元素的顺序
    random.shuffle(str_list)
    return ''.join(str_list)

def encrypt(key, string):
    """
    字符串加密函数
    :param key: 加密的key
    :param string: 要加密的字符串
    :return: 加密后的字符串
    """
    h = hmac.new(key.decode('utf-8'))
    h.update(string.decode('utf-8'))
    return h.hexdigest()


class MyThreadingTCPServer(socketserver.ThreadingTCPServer):
    def verify_request(self, request, client_address):
        """

        :param request: 连接socket,相当于conn
        :param client_address:
        :return:
        """
        request.sendall('请输入用户名'.encode('utf-8'))
        username = request.recv(1024)
        request.sendall('请输入密码'.encode('utf-8'))
        password = request.recv(1024)
        # 判断输入的用户名和密码是否和数据库的匹配
        if username == b'alex' and password == b'123456':
            request.sendall('登录成功'.encode('utf-8'))
            return True
        else:
            request.sendall('登录失败'.encode('utf-8'))
            return False


if __name__ == '__main__':
    # 这句代码创建socket,绑定地址,进行监听
    obj = MyThreadingTCPServer(('127.0.0.1', 13140), FTPServer)
    # 并进入链接循环进行accept
    obj.serve_forever()
