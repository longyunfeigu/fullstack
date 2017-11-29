#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
线程锁
GIL锁是加在进程上的，只允许一个线程同一时刻只能有一个线程被调度执行(即使有多核CPU),
而我们要加的锁是加在进程里面的

线程或进程什么时候切换：1. 遇到io操作  2. 运行了一段时间(具体是多长时间完全由操作系统决定)
"""
import threading
import time
"""
计算密集型

def counter():
    i = 0
    for _ in range(50000000):
        i += 1
    return i

if __name__ == '__main__':
    threads = []
    start_time = time.time()

    for i in range(2):
        # 串行，类似于单线程
        t = threading.Thread(target=counter)
        t.start()
        threads.append(t)
        t.join()

    # 多线程的并发
    # for t in threads:    # #等待所有线程执行完毕
    #     t.join()
    end_time = time.time()

    print('total time: ', end_time - start_time)
"""

"""
import threading
import time

num = 0
def addNUm():
    global num
    # num += 1
    temp = num
    time.sleep(0.3)
    num = temp + 1

thread_list = []

for i in range(100):
    t = threading.Thread(target=addNUm)
    t.start()
    thread_list.append(t)

for t in thread_list:
    t.join()

# 结果是1,没有得到想要的100
print(num)

注意：

1:  why num+=1没问题呢？这是因为动作太快(完成这个动作在切换的时间内)

2： if sleep(1),现象会更明显，100个线程每一个一定都没有执行完就进行了切换，
我们说过sleep就等效于IO阻塞，1s之内不会再切换回来，所以最后的结果一定是99.

多个线程都在同时操作同一个共享资源，所以造成了资源破坏，怎么办呢？

第一反应想用join呗，但join会把整个线程给停住，造成了串行，失去了多线程的意义，而我们只需要把计算(涉及到操作公共数据)的时候串行执行。
注意，我们仅仅是把计算串行执行
"""
import threading
import time

num = 0
lock = threading.Lock()   # 互斥锁

def addNUm():
    global num
    print(num)
    # num += 1
    lock.acquire()
    temp = num
    # 0.05秒可能足够cpu切换线程100次了
    time.sleep(0.05)
    num = temp + 1
    lock.release()

thread_list = []

for i in range(100):
    t = threading.Thread(target=addNUm)
    t.start()
    thread_list.append(t)

for t in thread_list:
    t.join()

# 100
print(num)