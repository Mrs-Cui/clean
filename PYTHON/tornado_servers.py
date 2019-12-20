#! /usr/bin/env
# -*- coding:utf-8 -*-

"""
    测试 tornado stack_context
"""
import contextlib
import functools
from tornado import stack_context
from tornado import ioloop
ioloop = ioloop.IOLoop.instance()

times = 0
"""
    捕获异步调用异常示例:
"""
# def callback():
#     print('run callback')
#     raise ValueError('except in callback')
#
#
# def wrapped(func):
#     try:
#         func()
#     except Exception as e:
#         print('main exception {}'.format(e))
#
# def async_task():
#     global times
#     times += 1
#     print('run async task {}'.format(times))
#     ioloop.add_callback(callback=functools.partial(wrapped, callback))
#
#
# def main():
#     try:
#         wrapped(async_task)
#     except Exception as e:
#         print(e)

"""
    测试 torando stack_context 捕获异步调用异常实例:
"""

# def callback():
#     print ('Run callback')
#     raise ValueError('except in callback')
#
# def async_task():
#     global times
#     times += 1
#     print('run async task {}'.format(times))
#     ioloop.add_callback(callback=callback)
#
# @contextlib.contextmanager
# def contextor():
#     print('Enter contextor')
#     try:
#         yield
#     except Exception as e:
#         # print('Handler except')
#         print('exception {}'.format(e))
#     finally:
#         print('Release')
#
# def main():
#     with stack_context.StackContext(contextor):
#         async_task()
#     print('End')


from tornado.tcpserver import TCPServer
from tornado import gen
from tornado.concurrent import Future


class MyTCPConnection(object):
    def __init__(self, stream, address, server):
        self.stream = stream
        self.address = address
        self.server = server

    def start_serving(self, future=None):
        future = self.stream.read_until("that is all!".encode())  # 在iostream中创建了一个异步读事件
        future.add_done_callback(self.message_recived)  # 在将message_recived作为该事件的回掉函数

    def message_recived(self, future):
        message = future.result().decode()
        print('messages', message)
        if message == "that is all!":  # 如果仅发送that is all!，则说明客户端消息已发送完毕
            print("no more messages")
            self.stream.close()
            self.server.on_conn_close(self)
            self.server = None
        else:
            print("data recieved: ", message)
            future = self.stream.write(message.encode())  # 在iostream中创建了一个异步写事件
            future.add_done_callback(self.start_serving)  # 时间出发说明写已完毕，所以回掉即为再次读消息的函数


class MyTCPServer(TCPServer):
    def __init__(self):
        super().__init__()
        self._conns = set()

    # tcpserver“连接已建立事件”的回掉函数
    def handle_stream(self, stream, address):
        conn = MyTCPConnection(stream, address, self)
        self._conns.add(conn)
        return conn.start_serving()

    def on_conn_close(self, conn):
        self._conns.remove(conn)


if __name__ == "__main__":
    server = MyTCPServer()
    server.listen(8001, '0.0.0.0')
    from tornado.ioloop import IOLoop

    IOLoop().current().start()


