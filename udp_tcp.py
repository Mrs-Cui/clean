#! /usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import argparse
import requests
import sys
import select, utils

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


# 异步服务器


def all_listen_event(poll):
    while True:
        for fd, event in poll.poll():
            yield fd, event

def server(listen):
    sockets = {listen.fileno(): listen}
    receive = {}
    send = {}
    poll = select.poll()
    poll.register(listen, select.POLLIN)
    for fd, event in all_listen_event(poll):
        sock = sockets[fd]
        if event and (select.POLLHUP or select.POLLNVAL or select.POLLERR):
            """
                开始接受/发送数据处理。
            """
            poll.unregister(sock)
            del sockets[fd]
        elif sock is listen:
            client_sock, address = sock.accept()
            client_sock.setblocking(False)
            sockets[client_sock.fileno] = client_sock
            poll.register(client_sock, client_sock.POOLIN)

        elif event and event.POOLIN:
            more_data = sock.recv(4096)
            if not more_data:
                sock.close()
                continue
            data = receive.pop(sock, b'') + more_data
            if more_data.endwith(b'?'):
                send[sock] = utils.get_answer(data)
                poll.modify(sock, sock.POLLOUT)
            else:
                receive[sock] = data
        elif event and event.POOLOUT:
            data = send.pop(sock, b'')
            n = sock.send(data)
            if n < len(data):
                send[sock] = data[n+1:]
            else:
                poll.modify(sock, sock.POLLIN)

if __name__ == '__main__':
    pass