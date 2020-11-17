#! /usr/bin/env python


#! /usr/bin/env python
import time
import sys
from tornado.httputil import HTTPServerRequest
from tornado.web import RequestHandler
from tornado.gen import coroutine, convert_yielded
from tornado.concurrent import is_future
from tornado.concurrent import raise_exc_info
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.httpclient import AsyncHTTPClient
from tornado.websocket import WebSocketHandler
from tornado import process, netutil, httpserver, ioloop, httpclient, httputil
from tornado.concurrent import Future, run_on_executor
from concurrent.futures import ThreadPoolExecutor
from tornado.queues import PriorityQueue, LifoQueue
from tornado.httpserver import HTTPServer

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
        fut = Future()
        def run() -> None:
            try:
                result = func(fut)
            except Exception:
                # fut = Future()  # type: Future[Any]
                # future_cell[0] = fut
                pass
            else:
                pass
                # if is_future(result):
                #     fut.set_result(result.result())
                # else:
                #     # fut = Future()
                #     # future_cell[0] = fut
                #     fut.set_result(result)

        ioloop.IOLoop.current().add_callback(run)
        return fut

    @coroutine
    def handle(self):
        resp = yield AsyncHTTPClient().fetch('http://www.gevent.org/')
        return resp

    @coroutine
    def execute(self, fut):
        conn = pymysql.connect(**CONFIG_CONNECT)
        cursor = conn.cursor()
        cursor.execute('select * from lbe_manager.ec2_and_user')
        try:
            result = yield cursor.fetchall()
        except:
            result = []
        fut.set_result(json.dumps(result))



    @coroutine
    def get(self, *args, **kwargs):
        future = yield self.new_handle(self.execute)
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
    process.fork_processes(os.cpu_count())
    server = httpserver.HTTPServer(app)
    server.add_sockets(sockets)
    print('测试开始')
    ioloop.IOLoop.current().start()