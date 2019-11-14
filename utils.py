#! /usr/bin/env python
# -*- coding:utf-8 -*-

import argparse, socket, time


def parse_command_line(description):
    parse = argparse.ArgumentParser(description=description)
    parse.add_argument('host', help='IP or hostname')
    parse.add_argument('-p', metavar='port', type=int, default=1060, help='TCP port')

    args = parse.parse_args()
    address = (args.host, args.p)
    return address


def create_tcp_socket(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(1024)
    return sock

def accept_connection(sock):

    while True:
        client_sock, address = sock.accept()
        handle_connection(client_sock, address)

def handle_connection(sock, address):

    try:
        handle_request(sock)
    except EOFError as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        sock.close()
def handle_request(sock):

    pass

def get_answer(data):
    pass


if __name__ == '__main__':
    pass

