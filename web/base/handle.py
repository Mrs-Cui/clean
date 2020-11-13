#! /usr/bin/env python


#! /usr/bin/env python
import time
import sys
from tornado.httputil import HTTPServerRequest
from tornado.web import RequestHandler
from tornado.gen import coroutine, convert_yielded
from tornado.concurrent import future_set_exc_info, is_future
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.websocket import WebSocketHandler
from tornado import process, netutil, httpserver, ioloop, httpclient, httputil
from tornado.concurrent import Future, run_on_executor
from concurrent.futures import ThreadPoolExecutor

import os
import json
import pymysql
import requests

CONFIG_CONNECT = {
    'host': '127.0.0.1',
    'port': 14449,
    'db': 'lbe_manager',
    'user': 'django',
    'password': 'Django.Password2020',
    'charset': 'utf8'
}


class BaseHandle(RequestHandler):

    max_thread_num = 20
    executor = ThreadPoolExecutor(max_workers=max_thread_num)

    def new_handle(self, func, timeout=None):
        future_cell = [None]

        def run() -> None:
            try:
                result = func()
            except Exception:
                fut = Future()  # type: Future[Any]
                future_cell[0] = fut
                future_set_exc_info(fut, sys.exc_info())
            else:
                if is_future(result):
                    future_cell[0] = result
                else:
                    fut = Future()
                    future_cell[0] = fut
                    fut.set_result(result)

        ioloop.IOLoop.current().add_callback(run)
        return future_cell[0]

    def handle(self):
        resp = requests.get('http://www.baidu.com')
        time.sleep(1)
        return resp.content

    @coroutine
    def get(self, *args, **kwargs):
        future = yield self.new_handle(self.handle)
        print('-' * 10, future)
        self.finish('hello world')

    def post(self, *args, **kwargs):

        pass


if __name__ == '__main__':
    app = Application(
        [
            (r'/handle', BaseHandle)
        ]
    )
    sockets = netutil.bind_sockets(6667, address='0.0.0.0', reuse_port=True)
    process.fork_processes(os.cpu_count() * 2)
    server = httpserver.HTTPServer(app)
    server.add_sockets(sockets)
    print('测试开始')
    ioloop.IOLoop.current().start()