#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
条件同步和条件变量同步差不多意思，只是少了锁功能，因为条件同步设计于不访问共享资源的条件环境。
event=threading.Event()：条件环境对象，初始值 为False；

event.isSet()：返回event的状态值；

event.wait()：如果 event.isSet()==False将阻塞线程；

event.set()： 设置event的状态值为True，所有阻塞池的线程激活进入就绪状态， 等待操作系统调度；

event.clear()：恢复event的状态值为False。
"""
"""
import threading
import time

class Boss(threading.Thread):
    def run(self):
        print('今天加班到10:00')
        event.is_set() or event.set()
        time.sleep(5)
        print('可以下班了')
        event.is_set() or event.set()
class Worker(threading.Thread):
    def run(self):
        event.wait()
        print(self.name, 'is 苦逼')
        time.sleep(0.25)
        event.clear()
        event.wait()
        print('OhYeah')

if __name__ == '__main__':
    event = threading.Event()
    thread_list = []
    for i in range(5):
        thread_list.append(Worker())
    thread_list.append(Boss())
    for t in thread_list:
        t.start()

    for t in thread_list:
        t.join()
"""

"""
import threading,time
import random

def light():
    event.is_set() or event.set()
    count = 0
    while 1:
        # 10s 绿灯
        if count < 10:
            print('\033[42;1m green light on\033[0m')
        # 3s 黄灯
        elif count < 13:
            print('\033[43;1m yellow light on\033[0m')
        # 7s 红灯
        elif count < 20:
            print('\033[41;1m--red light on---\033[0m')
            event.clear()
        # 一轮结束,计时重新开始，并开启绿灯
        else:
            event.set()   # 打开绿灯
            count = 0
        # count 模拟秒数
        time.sleep(1)
        count += 1


def car(n):
    # 每辆车用while循环来回搞
    sleep_time = random.randrange(10)
    while 1:
        time.sleep(sleep_time)
        if event.is_set():
            print("car [%s] is running.." % n)
        else:
            print("car [%s] is waiting for the red light.." %n)

if __name__ == '__main__':
    event = threading.Event()
    light_thread = threading.Thread(target=light)
    light_thread.start()
    car_list = []
    for i in range(2):
        car_list.append(threading.Thread(target=car, args=(i,)))
    for t in car_list:
        t.start()
"""