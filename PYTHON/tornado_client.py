#! /usr/bin/env python
# -*- coding:utf-8 -*-

import socket

from tornado.httpclient import HTTPClient
from tornado.httpserver import HTTPRequest


class Client(HTTPClient):
    pass


def client():
    sock = socket.socket()
    sock.connect(('127.0.0.1', 8001))
    sock.sendall(b'ni da ye!')
    message = sock.recv(1024)
    print(message)
if __name__ == '__main__':
    client()
