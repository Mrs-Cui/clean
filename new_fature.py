#! /usr/bin/env python
# -*- coding:utf-8 -*-
import os
import socket
from selectors import EVENT_WRITE, EVENT_READ
import selectors
from  concurrent.futures import ThreadPoolExecutor
selector = selectors.EpollSelector()

class Future(object):

    def __init__(self):
        self.result = ''
        self._callback = []

    def add_callback(self,func):
        self._callback.append(func)

    def set_result(self, result):
        self.result = result
        for func in self._callback:
            func(self)

class Crawler(object):

    def __init__(self, url):
        self.url = url
        self.response = ''


    def fetch(self):
        sock = socket.socket()
        sock.setblocking(False)

        try:
            sock.connect(('www.sina.com', 80))
        except BlockingIOError as e:
            pass
        f = Future()

        def on_connected():
            f.set_result(None)

        selector.register(sock.fileno(), EVENT_WRITE, on_connected)
        yield f
        selector.unregister(sock.fileno())
        get = 'GET {0} HTTP/1.0\r\nHost: www.sina.com\r\n\r\n'.format(self.url)
        sock.send(get.encode('ascii'))

        while True:

            f = Future()

            def read_table():
                f.set_result(sock.recv(4096))

            selector.register(sock.fileno(), EVENT_READ, read_table)




if __name__ == '__main__':
    import time
    import sys
    from threadpool import ThreadPool
    def a(i):
        time.sleep(i)
        print(os.getpid(), os.getppid())
        # print(sys.stdout)
        return i
    # pool = ThreadPoolExecutor(10)
    # queue = []
    # for i in pool.map(a, [i for i in range(10)],timeout=10):
    #     print(i)
    from multiprocessing import Pool, Process
    pool = Pool(10)
    for i in range(10):
        pool.apply_async(a, (i,))
    pool.close()
    pool.join()

