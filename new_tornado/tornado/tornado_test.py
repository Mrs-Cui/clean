# /usr/bin/env python
# -*- coding:utf-8 -*-


import traceback
import sys
import itertools
import time
from tornado import netutil, process
from tornado import httpserver, ioloop, gen, web
def traceback_test():
    try:
        raise IndexError()
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print('exc_type', exc_type, 'exc_value', exc_value, exc_traceback)
        # traceback.print_tb(exc_traceback, limit=1, file=sys.stderr)
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=1, file=sys.stdout)

class MainHandler(web.RequestHandler):

    def get(self):
        self.write('Hello, world')


class TestFutureHandler(web.RequestHandler):

    def get(self):
        print('request', self.request, type(self.request))
        self.write('how are you?')
        self.finish()

def tornado_test():
    application = web.Application([
        # (r'/', MainHandler),
        (r'/test', TestFutureHandler),
    ])
    sockets = netutil.bind_sockets(6667, address='0.0.0.0')
    process.fork_processes(1)
    server = httpserver.HTTPServer(application)
    server.add_sockets(sockets)
    print('测试开始')
    ioloop.IOLoop.current().start()

# @gen.coroutine
def decorate_test():
    while True:
        a = yield 'hello world'
        b = yield 'welcome to '
        return a, b
if __name__ == '__main__':
    import requests
    tornado_test()

