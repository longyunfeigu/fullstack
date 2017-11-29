#!/usr/lib/env python
# -*- coding: utf8 -*-
"""
Semaphore管理一个内置的计数器，
每当调用acquire()时内置计数器-1；
调用release() 时内置计数器+1；
计数器不能小于0；当计数器为0时，acquire()将阻塞线程直到其他线程调用release()。

实例：(同时只有5个线程可以获得semaphore,即可以限制最大连接数为5)：
"""

"""
import threading, time

def run(n):
    semaphore.acquire()
    time.sleep(1)
    print("run the thread: %s" % n)
    semaphore.release()

if __name__ == '__main__':

    num = 0
    semaphore = threading.BoundedSemaphore(5)  # 最多允许5个线程同时运行
    for i in range(20):
        t = threading.Thread(target=run, args=(i,))
        t.start()

while threading.active_count() != 1:
    pass  # print threading.active_count()
else:
    print('----all threads done---')
    print(num)
"""
from threading import *

def hello():
    print("hello, world")

# 3s之后执行函数
t = Timer(3.0, hello)
t.start()  # after 30 seconds, "hello, world" will be printed