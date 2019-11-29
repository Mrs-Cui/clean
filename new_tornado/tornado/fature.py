#! /usr/bin/env python
# -*- coding:utf-8 -*-

import socket
from concurrent import futures
from selectors import DefaultSelector,EVENT_WRITE,EVENT_READ
import asyncio
import aiohttp
import select
import selectors

selector = selectors.EpollSelector()
stopped = False
import time
from time import ctime


def tsfunc(func):
    def wrappedFunc(*args,**kargs):
        start = time.clock()
        action = func(*args,**kargs)
        time_delta = time.clock() - start
        print ('[{0}] {1}() called, time delta: {2}'.format(ctime(),func.__name__,time_delta))
        return action
    return wrappedFunc


def blocking_way():
    sock = socket.socket()
    sock.connect(('www.sina.com',80))
    request = 'GET / HTTP/1.0\r\nHOST:www.sina.com\r\n\r\n'
    sock.send(request.encode('ascii'))
    response = b''
    chunk = sock.recv(4096)
    while chunk:
        response += chunk
        chunk = sock.recv(4096)
    return response


@tsfunc
def sync_way():
    res = []
    for i in range(10):
        res.append(blocking_way())
    return len(res)
@tsfunc
# 阻塞、多进程
def process_way():
    worker = 10
    with futures.ProcessPoolExecutor(worker) as executor:
        futs = {executor.submit(blocking_way) for i in range(10)}
    len([fut.result() for fut in futs])
# 阻塞、多线程
@tsfunc
def thread_way():
    worker = 10
    with futures.ThreadPoolExecutor(worker) as executor:
        futs = {executor.submit(blocking_way) for i in range(10)}
    len([fut.result() for fut in futs])



class NewCrawler():

    def __init__(self, url):
        self.url = url
        self.sock = None
        self.response = ''


    def fetch(self):
        self.sock = socket.socket()
        self.sock.setblocking(False)
        try:
            self.sock.connect(('www.sina.com', 80))
        except BlockingIOError as e:
            pass
        selector.register(self.sock.fileno(), selectors.EVENT_WRITE, self.connect)

    def connect(self, key, mask):
        selector.unregister(self.sock.fileno())
        get = 'GET {0} HTTP/1.0\r\nHost:www.sina.com\r\n\r\n'.format(self.url)
        self.sock.send(get.encode('ascii'))
        selector.register(key.fd, selectors.EVENT_READ, self.read_response)

    def read_response(self, key, mask):
        global stopped
        while True:
            try:
                chunk = self.sock.recv(4096)
                if chunk:
                    self.response += chunk
                    chunk = self.sock.recv(4096)
                else:
                    selector.unregister(key.fd)
                    urls_todo.remove(self.url)
                    if not urls_todo:
                        stopped = True
                    break
            except:
                pass

def loop1():
    while not stopped:
        events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            callback(event_key, event_mask)

urls_todo = ['http://www.baidu.com',] * 50


@tsfunc
def callback_way():
    for url in urls_todo:
        crawler = NewCrawler(url)
        crawler.fetch()
    loop1()


# 基于生成器的协程
class Future:
    def __init__(self):
        self.result = None
        self._callbacks = []

    def add_done_callback(self, fn):
        self._callbacks.append(fn)

    def set_result(self, result):
        self.result = result
        for fn in self._callbacks:
            fn(self)


class Crawler1():
    def __init__(self, url):
        self.url = url
        self.response = b''

    def fetch(self):
        sock = socket.socket()
        sock.setblocking(False)
        try:
            sock.connect(('www.sina.com', 80))
        except BlockingIOError:
            pass

        f = Future()

        def on_connected():
            f.set_result(None)

        selector.register(sock.fileno(), EVENT_WRITE, on_connected)
        yield f
        selector.unregister(sock.fileno())
        get = 'GET {0} HTTP/1.0\r\nHost: www.sina.com\r\n\r\n'.format(self.url)
        sock.send(get.encode('ascii'))

        global stopped
        while True:
            f = Future()

            def on_readable():
                f.set_result(sock.recv(4096))

            selector.register(sock.fileno(), EVENT_READ, on_readable)
            chunk = yield f
            selector.unregister(sock.fileno())
            if chunk:
                self.response += chunk
            else:
                urls_todo.remove(self.url)
                if not urls_todo:
                    stopped = True
                break


# yield from 改进的生成器协程
class Future1:
    def __init__(self):
        self.result = None
        self._callbacks = []

    def add_done_callback(self, fn):
        self._callbacks.append(fn)

    def set_result(self, result):
        self.result = result
        for fn in self._callbacks:
            fn(self)

    def __iter__(self):
        yield self
        return self.result


def connect(sock, address):
    f = Future1()
    sock.setblocking(False)
    try:
        sock.connect(address)
    except BlockingIOError:
        pass

    def on_connected():
        f.set_result(None)

    selector.register(sock.fileno(), EVENT_WRITE, on_connected)
    yield from f
    selector.unregister(sock.fileno())


def read(sock):
    f = Future1()

    def on_readable():
        f.set_result(sock.recv(4096))

    selector.register(sock.fileno(), EVENT_READ, on_readable)
    chunk = yield from f
    selector.unregister(sock.fileno())
    return chunk


def read_all(sock):
    response = []
    chunk = yield from read(sock)
    while chunk:
        response.append(chunk)
        chunk = yield from read(sock)
    return b''.join(response)


class Crawler2:
    def __init__(self, url):
        self.url = url
        self.response = b''

    def fetch(self):
        global stopped
        sock = socket.socket()
        yield from connect(sock, ('www.sina.com', 80))
        get = 'GET {0} HTTP/1.0\r\nHost: www.sina.com\r\n\r\n'.format(self.url)
        sock.send(get.encode('ascii'))
        self.response = yield from read_all(sock)
        urls_todo.remove(self.url)
        if not urls_todo:
            stopped = True


class Task:
    def __init__(self, coro):
        self.coro = coro
        f = Future1()
        f.set_result(None)
        self.step(f)

    def step(self, future):
        try:
            # send会进入到coro执行, 即fetch, 直到下次yield
            # next_future 为yield返回的对象
            next_future = self.coro.send(future.result)
        except StopIteration:
            return
        next_future.add_done_callback(self.step)


def loop2():
    while not stopped:
        events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            callback()

@tsfunc
def callback_way():
    for url in urls_todo:
        crawler = Crawler2(url)
        coro = crawler.fetch()
        task = Task(coro)
    loop2()

if __name__ == '__main__':
    # sync_way() # 0.00631799999999999
    # process_way()
    # thread_way() # 0.004729000000000011
    callback_way()