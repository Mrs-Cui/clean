#! /usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import


from abc import ABC
from gevent.pool import Pool


__all__ = [
    'A',
    'B'
]
import gevent

class A(object):

    def __init__(self):
        self.a = '靠'

    def add(self, a, b):
        temp = a + b
        print('add', temp)

    def __getattribute__(self, item):
        print('getattribute','A', self, item)
        return object.__getattribute__(self,item)


class B(A):

    def get_b(self):
        print(self.a)

class RevealAccess(A):
    """A data descriptor that sets and returns values
       normally and prints a message logging their access.
    """

    def __init__(self, initval=None, name='var'):
        self.val = initval
        self.name = name

    def __getattribute__(self, item):
        print('getattribute', item)

        return object.__getattribute__(self, item)


    def __get__(self, instance, owner):
        print("__get__() is called", self, instance, owner)
        print('Retrieving', self.name, self.val)
        return self
    #
    # def __set__(self, obj, val):
    #     print('Updating', self.name)
    #     self.val = val


    def __delete__(self, instance):
        print('delete', instance.x)

class MyClass(dict):
    x = RevealAccess(10, 'var "x"')
    y = 5

    def __init__(self, x=None):
        self.b = x
        pass
    @staticmethod
    def a(*args):
        print(MyClass.a.__name__)

import time

def product(food):

    while True:

        if not food:
            con = consume(food)
            next(con)
            food.extend([1, 2, 3])
            print(product.__name__, food)
            con.send(food)
        elif len(food) >= 100:
            time.sleep(2)
        else:
            food.extend([1, 2, 3])
        print(food)

def consume(food):

    while True:

        if not food:
            food = (yield)
            print(consume.__name__, food)
        else:
            print(consume.__name__, food)
            food.pop()

import asyncio
import contextvars
# from asyncio.runners import run


client_addr_var = contextvars.ContextVar('client_addr')

def render_goodbye():
    # The address of the currently handled client can be accessed
    # without passing it explicitly to this function.

    client_addr = client_addr_var.get()
    return f'Good bye, client @ {client_addr}\n'.encode()

async def handle_request(reader, writer):
    addr = writer.transport.get_extra_info('socket').getpeername()
    client_addr_var.set(addr)
    print(type(reader), type(writer), addr)
    # In any code that we call is now possible to get
    # client's address by calling 'client_addr_var.get()'.

    while True:
        line = await reader.readline()
        print(line)
        if not line.strip():
            break
        writer.write(line)

    writer.write(render_goodbye())
    writer.close()


async def main():
    srv = await asyncio.start_server(
        handle_request, '127.0.0.1', 8081)

    async with srv:
        await srv.serve_forever()

import types
import time

@types.coroutine
def clear():
    print('clean!!')
    time.sleep(1)
    a = yield from(1, 2, 3)
    print('a', a)
    print(1)
    b = yield from(4, 5, 6)
    print('b', b)
    return True


from functools import wraps

from tornado import platform
from tornado import wsgi
from tornado import httpserver
from tornado import ioloop
def application():
    return 'hello world'

from gevent import pool
pool.Pool()

if __name__ == '__main__':
    pass
