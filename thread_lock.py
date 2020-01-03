import time
import threading

# 生成一个递归对象
Rlock = threading.RLock()


class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self) -> None:
        print('thread ident', threading.current_thread().ident)
        self.fun_A()
        self.fun_B()

    def fun_A(self):
        Rlock.acquire()
        print('A加锁1', end='\t')
        Rlock.acquire()
        print('A加锁2', end='\t')
        time.sleep(3)
        Rlock.release()
        print('A释放1', end='\t')
        Rlock.release()
        print('A释放2')

    def fun_B(self):
        Rlock.acquire()
        print('B加锁1', end='\t')
        Rlock.acquire()
        print('B加锁2', end='\t')
        time.sleep(3)
        Rlock.release()
        print('B释放1', end='\t')
        Rlock.release()
        print('B释放2')


import time
import threading


def semaphore_test():

    # 生成一个锁对象
    semaphore = threading.Semaphore(1)  # 创建信号量对象，5个线程并发
    lock = threading.Lock()

    def func():
        nonlocal num  # 全局变量
        lock.acquire()  # 获得锁，加锁
        num1 = num
        time.sleep(0.1)
        num = num1 - 1
        semaphore.release()  # 释放锁，解锁
        time.sleep(2)


    num = 100
    l = []

    for i in range(100):  # 开启100个线程
        t = threading.Thread(target=func, args=())
        t.start()
        l.append(t)

    # 等待线程运行结束
    for i in l:
        i.join()

    print(num)


def condition_test():
    import threading
    import time

    # 商品
    product = None
    # 条件变量对象
    con = threading.Condition()

    # 生产方法
    def produce():
        nonlocal product  # 全局变量产品
        if con.acquire():
            while True:
                print('---执行，produce--')
                if product is None:
                    product = '袜子'
                    print('---生产产品:%s---' % product)
                    # 通知消费者，商品已经生产
                    con.notify()  # 唤醒消费线程
                # 等待通知
                con.wait()
                time.sleep(2)

    # 消费方法
    def consume():
        nonlocal product
        if con.acquire():
            while True:
                print('***执行，consume***')
                if product is not None:
                    print('***卖出产品:%s***' % product)
                    product = None
                    # 通知生产者，商品已经没了
                    con.notify()
                # 等待通知
                con.wait()
                time.sleep(2)

    t1 = threading.Thread(target=consume)
    t1.start()
    t2 = threading.Thread(target=produce)
    t2.start()

def queue_test():
    import threading, time
    import queue

    # 最多存入10个
    q = queue.PriorityQueue(10)

    def producer(name):
        ''' 生产者 '''
        count = 1
        while True:
            # 　生产袜子
            q.put("袜子 %s" % count)  # 将生产的袜子方法队列
            print(name, "---生产了袜子", count)
            count += 1
            time.sleep(0.2)

    def consumer(name):
        ''' 消费者 '''
        while True:
            print("%s ***卖掉了[%s]" % (name, q.get()))  # 消费生产的袜子
            time.sleep(1)
            q.task_done()  # 告知这个任务执行完了

    # 生产线程
    z = threading.Thread(target=producer, args=("张三",))
    # 消费线程
    l = threading.Thread(target=consumer, args=("李四",))
    w = threading.Thread(target=consumer, args=("王五",))

    # 执行线程
    z.start()
    l.start()
    w.start()


class Score(object):

    def __init__(self, default=0):
        self.score = default

    def __set__(self, instance, value):
        print('set', self, instance, value)
        instance.score = value

    def __get__(self, instance, owner):
        print('get', self, instance, owner)

        return instance.score


class PythonFeature(object):

    math = Score(0)
    english = Score(0)

    def __init__(self, math, english):
        self.math = math
        self.english = english

    # def __setattr__(self, key, value):
    #     print('attr', key, value)
    #     self.__dict__[key] = value
    #
    # def __setitem__(self, key, value):
    #     print('item', key, value)
    #     self.__dict__[key] = value


    def hello(self):
        print('hello world')

if __name__ == '__main__':
    p = PythonFeature(11, 12)
    print(type(p.math), dir(p.math))
    print(p.math)
