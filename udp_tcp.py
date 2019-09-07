#! /usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import argparse
import requests

def server():
    HOST = '127.0.0.1'
    PORT = 21567
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(20)

    client_socket, addr = server_socket.accept()
    # while True:
    #     client_socket = server_socket.accept()
    #
    #     print(type(client_socket))
    #     break


def client():
    pass


if __name__ == '__main__':
    requests.get('http://www.baidu.com')