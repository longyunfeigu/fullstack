#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
import threading,time

class myThread(threading.Thread):
    def doA(self):
        lockA.acquire()
        print(self.name,"gotlockA",time.ctime())
        time.sleep(3)
        lockB.acquire()
        print(self.name,"gotlockB",time.ctime())
        lockB.release()
        lockA.release()

    def doB(self):
        lockB.acquire()
        print(self.name,"gotlockB",time.ctime())
        # 这个sleep的时候切换到另一个线程，切换到另一个线程，另一个线程获得A锁
        # 造成的结果就是一个线程拿了A锁，想要B锁，另一个线程拿了B锁，想要A锁，这样在没有外力的作用下造成死锁
        time.sleep(2)
        lockA.acquire()
        print(self.name,"gotlockA",time.ctime())
        lockA.release()
        lockB.release()
    def run(self):
        self.doA()
        self.doB()
if __name__=="__main__":

    lockA=threading.Lock()
    lockB=threading.Lock()
    threads=[]
    for i in range(3):
        threads.append(myThread())
    for t in threads:
        t.start()
    for t in threads:
        t.join()
"""

"""
import threading
import time

# rlock可以看作是内部维护了一个计数器，只有计数器为0的时候才能被acquire
rlock = threading.RLock()

class myThread(threading.Thread):
    def doA(self):
        rlock.acquire()
        print(self.name,"gotlockA",time.ctime())
        time.sleep(3)
        rlock.acquire()
        print(self.name,"gotlockB",time.ctime())
        rlock.release()
        rlock.release()

    def doB(self):
        rlock.acquire()
        print(self.name,"gotlockB",time.ctime())
        # 这个sleep的时候切换到另一个线程，切换到另一个线程，因为rlock的内部计数器不是0
        # 这样程序就不会因为死锁而卡住了
        time.sleep(2)
        rlock.acquire()
        print(self.name,"gotlockA",time.ctime())
        rlock.release()
        rlock.release()
    def run(self):
        self.doA()
        self.doB()
if __name__=="__main__":

    lockA=threading.Lock()
    lockB=threading.Lock()
    threads=[]
    for i in range(3):
        threads.append(myThread())
    for t in threads:
        t.start()
    for t in threads:
        t.join()
"""

