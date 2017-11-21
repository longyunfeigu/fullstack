#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import struct
import json
import os
# import socketserver

class FTPServer:
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 5
    max_package_size = 8192
    coding = 'utf-8'
    allow_reuse_address = False
    server_dir = '/tmp/file_upload'

    def __init__(self, server_address, bind_and_activate=True):
        """Constructor.  May be extended, do not override."""
        self.server_address = server_address
        self.socket = socket.socket(self.address_family, self.socket_type)

        if bind_and_activate:
            try:
                self.server_bind()
                self.server_activate()
            except:
                self.server_close()
                raise

    def server_bind(self):
        """Called by constructor to bind the socket.

           May be overridden.
        """
        if self.allow_reuse_address:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)
        self.server_address = self.socket.getsockname()

    def server_activate(self):
        """Called by constructor to activate the server.
            May be overridden.
        """
        self.socket.listen(self.request_queue_size)

    def server_close(self):
        """Called to clean-up the server.
        May be overridden.
        """
        self.socket.close()

    def get_request(self):
        """Get the request and client address from the socket.

            May be overridden.
        """
        return self.socket.accept()

    def close_request(self, request):
        """Called to clean up an individual request."""
        request.close()

    def shutdown_request(self, request):
        """Called to shutdown and close an individual request."""
        try:
            # explicitly shutdown.  socket.close() merely releases
            # the socket and waits for GC to perform the actual close.
            request.shutdown(socket.SHUT_WR)
        except OSError:
            pass  # some platforms may raise ENOTCONN here
        self.close_request(request)

    def run(self):
        """merely processing service"""
        while True:   # 链接循环
            self.conn, self.client_addr = self.get_request()
            print('from client...', self.client_addr)
            while True:
                try:
                    headers_struct = self.conn.recv(4)
                    if not headers_struct:
                        break
                    # server收取头信息
                    headers_length = struct.unpack('i', headers_struct)[0]
                    print('***********', headers_length)
                    headers_json = self.conn.recv(headers_length)
                    print('-------', headers_json)
                    headers_dict = json.loads(headers_json)
                    print('***********', headers_dict)

                    command = headers_dict.get('command')
                    if hasattr(self, command):
                        func = getattr(self, command)
                        func(headers_dict)
                except Exception as e:
                    break

    def put(self, args):
        filename = args.get('filename')
        filesize = args.get('filesize')
        file_path = os.path.join(self.server_dir, filename)
        already_recv_size = 0
        with open(file_path, 'wb') as f:
            while already_recv_size < filesize:
                recv_data = self.conn.recv(self.max_package_size)
                f.write(recv_data)
                already_recv_size += len(recv_data)
            else:
                print('download success')
    def get(self, args):
        filename = args.get('filename')
        filepath = os.path.join(self.server_dir, filename)
        print(filepath)
        if not os.path.exists(filepath):
            err_msg = '服务器没有该文件'
            headers_dict = {'err_msg': err_msg}
        else:
            filesize = os.path.getsize(filepath)
            headers_dict = {'command': args[0], 'filename': filename, 'filesize': filesize}
        # 发送数据之前先发数据的头信息
        headers_str = json.dumps(headers_dict)
        headers_bytes = headers_str.encode(self.coding)
        headers_length = len(headers_bytes)
        self.socket.send(struct.pack('i', headers_length))
        self.socket.send(headers_bytes)
        print('pppppppp')
        send_size = 0
        with open(filepath, 'rb') as f:
            print('write.....')
            for line in f:
                already_send_size = len(line)
                self.conn.send(line)
                send_size += already_send_size
                print(send_size)




if __name__ == '__main__':
    ftp_server = FTPServer(('10.20.1.50', 13140))
    ftp_server.run()
