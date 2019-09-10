#! /usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import argparse
import requests
import sys

def server():
    HOST = '127.0.0.1'
    PORT = 21567
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    client_socket, addr = server_socket.accept()
    # while True:
    #     client_socket = server_socket.accept()
    #
    #     print(type(client_socket))
    #     break


def client():
    pass


# makefile
import threading, logging

DATEFMT = "%H:%M:%S"
FORMAT = "[%(asctime)s]\t [%(threadName)s,%(thread)d] %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt=DATEFMT)

sock = socket.socket()
addr = ('127.0.0.1', 9999)
event = threading.Event()

sock.bind(addr)
sock.listen(1)
def _accept(sock):
    s, addrinfo = sock.accept()
    f = s.makefile(mode='rw')

    while True:
        line = f.readline()  # read(10) 文本使用readline
        logging.info(line)

        if line.strip() == 'quit':
            break

        msg = "Your msg = {}. ack".format(line)
        f.write(msg)
        f.flush()
    f.close()
    sock.close()


threading.Thread(target=_accept, args=(sock,)).start()

while not event.wait(2):
    logging.info(sock)


if __name__ == '__main__':
    pass