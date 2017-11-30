#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
我们以前学习的数据类型都是非线程安全的，例如两个线程对列表的某个元素赋值，
因为cpu切换的顺序不是我们可以预料的，所以可能得到的结果是线程1赋的值，也可能是线程2赋的值

queue这种数据类型是线程安全的

生产者消费者模型是一种编程思想，为了解决生产者和消费者的强耦合问题，借助queue这种数据类型来实现

创建一个“队列”对象
import Queue
q = Queue.Queue(maxsize = 10)
Queue.Queue类即是一个队列的同步实现。队列长度可为无限或者有限。可通过Queue的构造函数的可选参数maxsize来设定队列长度。如果maxsize小于1就表示队列长度无限。

将一个值放入队列中
q.put(10)
调用队列对象的put()方法在队尾插入一个项目。put()有两个参数，第一个item为必需的，为插入项目的值；第二个block为可选参数，默认为
1。如果队列当前为空且block为1，put()方法就使调用线程暂停,直到空出一个数据单元。如果block为0，put方法将引发Full异常。

将一个值从队列中取出
q.get()
调用队列对象的get()方法从队头删除并返回一个项目。可选参数为block，默认为True。如果队列为空且block为True，get()就使调用线程暂停，直至有项目可用。如果队列为空且block为False，队列将引发Empty异常。

Python Queue模块有三种队列及构造函数:
1、Python Queue模块的FIFO队列先进先出。  class queue.Queue(maxsize)
2、LIFO类似于堆，即先进后出。             class queue.LifoQueue(maxsize)
3、还有一种是优先级队列级别越低越先出来。   class queue.PriorityQueue(maxsize)

此包中的常用方法(q = Queue.Queue()):
q.qsize() 返回队列的大小
q.empty() 如果队列为空，返回True,反之False
q.full() 如果队列满了，返回True,反之False
q.full 与 maxsize 大小对应
q.get([block[, timeout]]) 获取队列，timeout等待时间
q.get_nowait() 相当q.get(False)
非阻塞 q.put(item) 写入队列，timeout等待时间
q.put_nowait(item) 相当q.put(item, False)
q.task_done() 在完成一项工作之后，q.task_done() 函数向任务已经完成的队列发送一个信号
q.join() 实际上意味着等到队列为空，再执行别的操作
"""

"""
import threading
import queue
from random import randint
import time

class Production(threading.Thread):
    def run(self):
        while 1:
            r = randint(0,100)
            q.put(r)
            print('\033[32;1m生产出来%s号包子\033[0m'%r)
            time.sleep(1)

class Consumer(threading.Thread):
    def run(self):
        while 1:
            re = q.get()
            print("\033[33;1m吃掉%s号包子\033[0m" % re)

if __name__ == '__main__':
    q = queue.Queue()
    threads = [Production(), Production(), Consumer()]
    for t in threads:
        t.start()
"""

"""
开两个线程一个线程循环20次地往队列里面放数据，另一个循环20次去取数据，当然两者之间肯定存在时间差

import threading
import queue
import time
import random

def producer(name):
    count = 0
    while count < 20:
        # 模拟生产包子的时间
        time.sleep(random.randrange(3))
        q.put(count)
        print('\033[32;1mProducer %s has produced %s baozi..\033[0m'%(name, count))
        count += 1

def consumer(name):
    count = 0
    while count < 20:
        if not q.empty():
            data = q.get()
            print(data)
            print('\033[33;1mConsumer %s has eat %s baozi...\033[0m' % (name, data))
        else:
            print("-----no baozi anymore----")
        count += 1
        # 吃完休息一下
        time.sleep(random.randrange(4))


if __name__ == '__main__':
    q = queue.Queue()
    t1 = threading.Thread(target=producer, args=('A',))
    t1.start()
    t1 = threading.Thread(target=consumer, args=('',))
    t1.start()
"""

# import random,threading,time
# from queue import Queue
# #Producer thread
# class Producer(threading.Thread):
#   def __init__(self, t_name, queue):
#     threading.Thread.__init__(self,name=t_name)
#     self.data=queue
#   def run(self):
#     for i in range(10):  #随机产生10个数字 ，可以修改为任意大小
#       randomnum=random.randint(1,99)
#       print ("%s: %s is producing %d to the queue!" % (time.ctime(), self.getName(), randomnum))
#       self.data.put(randomnum) #将数据依次存入队列
#       time.sleep(1)
#     print ("%s: %s finished!" %(time.ctime(), self.getName()))
#
# #Consumer thread
# class Consumer_even(threading.Thread):
#   def __init__(self,t_name,queue):
#     threading.Thread.__init__(self,name=t_name)
#     self.data=queue
#   def run(self):
#     while 1:
#       try:
#         val_even = self.data.get(1,5) #get(self, block=True, timeout=None) ,1就是阻塞等待,5是超时5秒
#         if val_even%2==0:
#           print ("%s: %s is consuming. %d in the queue is consumed!" % (time.ctime(),self.getName(),val_even))
#           time.sleep(2)
#         else:
#           self.data.put(val_even)
#           time.sleep(2)
#       except:   #等待输入，超过5秒 就报异常
#         print ("%s: %s finished!" %(time.ctime(),self.getName()))
#         break
# class Consumer_odd(threading.Thread):
#   def __init__(self,t_name,queue):
#     threading.Thread.__init__(self, name=t_name)
#     self.data=queue
#   def run(self):
#     while 1:
#       try:
#         val_odd = self.data.get(1,5)
#         if val_odd%2!=0:
#           print ("%s: %s is consuming. %d in the queue is consumed!" % (time.ctime(), self.getName(), val_odd))
#           time.sleep(2)
#         else:
#           self.data.put(val_odd)
#           time.sleep(2)
#       except:
#         print ("%s: %s finished!" % (time.ctime(), self.getName()))
#         break
# #Main thread
# def main():
#   queue = Queue()
#   producer = Producer('Pro.', queue)
#   consumer_even = Consumer_even('Con_even.', queue)
#   consumer_odd = Consumer_odd('Con_odd.',queue)
#   producer.start()
#   consumer_even.start()
#   consumer_odd.start()
#   producer.join()
#   consumer_even.join()
#   consumer_odd.join()
#   print ('All threads terminate!')
#
# if __name__ == '__main__':
#   main()

import queue
import threading
import time
import random

class Producer(threading.Thread):
    def __init__(self, name, q):
        threading.Thread.__init__(self, name=name)
        self.data = q

    def run(self):
        for i in range(10):
            time.sleep(1)
            random_data = random.randrange(10)
            print("%s: %s is producing %d to the queue!" % (time.ctime(), self.getName(), random_data))
            self.data.put(random_data)
        print("%s: %s finished!" % (time.ctime(), self.getName()))

class Con_odd(threading.Thread):
    def __init__(self, name, q):
        threading.Thread.__init__(self, name=name)
        self.data = q

    def run(self):
        while 1:
            try:
                val_odd = self.data.get(1,5)
                print(time.ctime(),'val_odd')
                if val_odd % 2 == 0:
                    self.data.put(val_odd)
                else:
                    print("%s: %s is consuming. %d in the queue is consumed!" % (time.ctime(), self.getName(), val_odd))
            except Exception as e:
                print("%s: %s finished!" % (time.ctime(), self.getName()))
                break
            else:
                time.sleep(2)


class Con_even(threading.Thread):
    def __init__(self, name, q):
        threading.Thread.__init__(self, name=name)
        self.data = q

    def run(self):
        while 1:
            try:
                val_even = self.data.get(1,5)
                print(time.ctime(), 'val_even')
                if val_even % 2 == 0:
                    print("%s: %s is consuming. %d in the queue is consumed!" % (time.ctime(), self.getName(), val_even))
                else:
                    self.data.put(val_even)
            except Exception as e:
                print("%s: %s finished!" % (time.ctime(), self.getName()))
                break
            else:
                time.sleep(2)

if __name__ == '__main__':
    print(time.ctime())
    q = queue.Queue()
    p = Producer('Pro', q)
    p.start()
    con_odd = Con_odd('con_odd', q)
    con_odd.start()
    con_even = Con_even('con_even', q)
    con_even.start()
    p.join()
    con_even.join()
    con_odd.join()
    print('All threads terminate!')


