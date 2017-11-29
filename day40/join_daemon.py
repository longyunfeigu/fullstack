#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
join和setDeamon

join是串行,参数表示阻塞几秒

守护线程的一个应用是日志系统，当程序运行的时候会产生日志，程序退出的时候日志记录也会跟着终止
"""
import threading
import time

def music(arg):
    print("Begin listening to %s. %s" %(arg,time.time()))
    time.sleep(3)
    print("end listening %s" % time.time())

def movie(arg):
    print("Begin watching to %s. %s" %(arg,time.time()))
    time.sleep(6)
    print("end watching %s" % time.time())

threads = []
t2 = threading.Thread(target=movie, args=('大话西游',))
t1 = threading.Thread(target=music, args=('青花瓷',))
threads.append(t1)
threads.append(t2)

if __name__ == '__main__':
    # t1.setDaemon(True)
    for t in threads:
        t.start()
        # t.join()  串行,多线程失去意义，而且比一般的串行更耗费时间，耗费的时间是cpu不断切换的时间，这种情况在py2中体现的很明显，
        # 但是在py3中做了优化，让这种形式的多线程和单线程的串行花费差不多的时间
    #
    # for t in threads:
    #     t.join()
    #     print('ok')
    # 因为两个线程已经在上一个循环中启动了，所以这样只花费了最大耗时的线程消耗的时间
    # 在子线程完成运行之前，这个子线程的父线程将一直被阻塞,注意阻塞的是父线程，不影响其他线程


    print('ending...', time.time())
"""
t1.setDaemon(True)结果是这样的
Begin watching to 大话西游. 1511916754.4842114
Begin listening to 青花瓷. 1511916754.4842114
ending... 1511916754.4842114
end listening 1511916757.4842114
Begin listening to 青花瓷. 1511916757.4842114
end watching 1511916758.4842114
Begin watching to 大话西游. 1511916758.4842114
end listening 1511916760.4842114

为什么t1设置成了守护线程并没有和主线程一起结束，而是等待3秒后才结束，因为t2没有设置成守护线程，所以主线程其实并没有结束

守护线程的意思就算follow me，我退出你就跟随我退出
"""



