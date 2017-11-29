#!/usr/bin/env pyhton
# -*-coding:utf8 -*-
"""
线程调用的两种方式
"""
import threading
import time
"""
class MyThread(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num

    def run(self): #定义每个线程要运行的函数
        print("running on number:%s" % self.num)
        time.sleep(3)

if __name__ == '__main__':
    t1 = MyThread(1)
    t2 = MyThread(2)
    t1.start()
    t2.start()
"""

def sayhi(num):
    """
    线程要运行的函数
    :param num:
    :return:
    """
    print("running on number:%s" % num)
    time.sleep(3)

if __name__ == '__main__':
    # 生成线程实例
    t1 = threading.Thread(target=sayhi, args=(1, ))
    t1.setName('t1_thread')
    t2 = threading.Thread(target=sayhi, args=(2, ))

    # 启动线程，等待cpu调度
    t1.start()
    t2.start()

    print(t1.getName())
    print(t2.getName())
    print(t1.is_alive())
    print(threading.current_thread())  # <_MainThread(MainThread, started 5196)>
    print(threading.current_thread().getName())  # <_MainThread(MainThread, started 5196)>
    print(threading.currentThread) # <function current_thread at 0x02464E40>
    print(threading.enumerate()) # [<_MainThread(MainThread, started 5196)>, <Thread(t1_thread, started 5236)>, <Thread(Thread-2, started 5960)>]
    print(threading.active_count()) # 3
