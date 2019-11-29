#! /usr/bin/env python
# -*- coding:utf-8 -*-
from gevent import monkey
monkey.patch_all()

from gevent.pool import Pool

class UserInfo(object):

    def __init__(self):
        pass

    def __getattribute__(self, item):
        try:
            key = object.__getattribute__(self, item)
        except AttributeError as e:
            return None
        return key

    def __getattr__(self, item):
        print(item)
        return item

    def get(self, name, default=None):
        value = self.__getattribute__(name)
        if not value:
            value = self.__getattr__(default)
        return value


from tornado.ioloop import PollIOLoop, IOLoop
from tornado.concurrent import run_on_executor
import requests
from tornado import gen
import types

@gen.coroutine
def main():
    return requests.get('http://www.baidu.com', proxies= {'http':'socks5://127.0.0.1:1080/', 'https': 'socks5://127.0.0.1:1080/'})

@gen.coroutine
def temp_a():

    return requests.get('http://www.baidu.com', proxies= {'http':'socks5://127.0.0.1:1080/', 'https': 'socks5://127.0.0.1:1080/'})



import logging.config
import logging.handlers

def config_logger():
    logging.handlers.TimedRotatingFileHandler
    config_class = logging.config.dictConfigClass()
    config_info = {

    }


import pymysql

from pika.adapters.tornado_connection import TornadoConnection
from tornado.ioloop import IOLoop
from pika.connection import Parameters

def error_callback():
    print('connection error!!!')

def connection():
    conn = TornadoConnection(parameters=Parameters(), on_open_callback=error_callback, on_open_error_callback=error_callback, custom_ioloop=IOLoop.current())

    print(conn)

import base64


import abc

class Tornado(metaclass=abc.ABCMeta):

    def like(self):
        print('like hello world!')




class Iter(object):

    def __init__(self, data=None):
        self.data = data
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.count < len(self.data):
            data = self.data[self.count]
            self.count += 1
            return data
        else:
            raise StopIteration


class OS(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def os_post(self):
        pass


class ChildOs(OS):


    def os_post(self):
        hello = yield 'hello'
        print('hello:', hello)
        yield 'world'


class Column(object):

    def __new__(cls, *args, **kwargs):
        pass

    def __set__(self, instance, value):
        pass

class Integer(Column):
    pass


class Float(Column):
    pass

class String(Column):
    pass

class UserAccount(object):

    jid = ''

    def __new__(cls, *args, **kwargs):
        print('new user account')
        return object.__new__(String)


class TreeNode(object):

    def __init__(self, data: str) ->None:
        self.data = data
        self.left = None
        self.right = None

def height(root):
    if not root:
        return 0
    h_left = height(root.left) + 1
    h_right = height(root.right) + 1
    h = max(h_left, h_right)
    return h


def create_tree(data, root=None):
    if not root:
        root = TreeNode(data)
    else:
        if data <= root.data:
            root = create_tree(data, root.left)
        else:
            root = create_tree(data, root.right)

        if height(root.left) - height(root.right) >= 2:
            pass

        if height(root.left) - height(root.right) <= -2:
            pass

    return root


import random

def tree():

    root = None
    for key in [random.randint(1, 20) for i in range(10)]:
        root = create_tree(key, root)


from tornado import httpserver, httpclient
from tornado import tcpclient, tcpserver, ioloop
from tornado import gen
from tornado.platform import epoll

class TcpServer(tcpserver.TCPServer):


    def __init__(self, port, address):
        self.port = port
        self.address = address
        super(TcpServer, self).__init__()
        self.init(self.port, self.address)

    def init(self, port, address):
        self.bind(port, address)


    @gen.coroutine
    def handle_stream(self, stream, address):
        pass

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)


class TcpClient(tcpclient.TCPClient):
    pass





from multiprocessing import Process, Queue, Pipe



def read(queue):
    print('start read!')
    # print('full:', queue.full())
    print('size:', queue.qsize())
    while queue.qsize():
        print('read:', queue.get_nowait(), 'qsize:', queue.qsize())


def write(queue, contents):
    for content in contents:
        print('write:', content)
        queue.put(content)
from multiprocessing import Process, Queue, Pool
import os,time,random



if __name__ == '__main__':
    #父进程创建Queue，并传给各个子进程
    pool = Pool()
    pool.apply_async()
