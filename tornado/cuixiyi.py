#! /usr/bin/env python
# -*- coding:utf-8 -*-

from tornado import gen
from tornado import concurrent

@gen.coroutine
def decorate_test():
    while True:
        # a = yield concurrent.Future()
        # b = yield concurrent.Future()
        print('decorate_test')
        yield read_response()


def read_response():
    print('read_response')
    return read_message()

@gen.coroutine
def read_message():
    print('read_message')
    yield concurrent.Future()


if __name__ == '__main__':
    import requests
    decorate_test()
