#! /usr/bin/env python
# -*- coding:utf-8 -*-

import errno
import os
import socket
import ssl

from tornado import gen
from tornado.log import app_log
from tornado.ioloop import IOLoop
from tornado.iostream import IOStream, SSLIOStream
from tornado.netutil import bind_sockets, add_accept_handler, ssl_wrap_socket
from tornado import process
from tornado.util import errno_from_exception

import typing
from typing import Union, Dict, Any, Iterable, Optional, Awaitable

if typing.TYPE_CHECKING:
	from typing import Callable, List  # noqa: F401


class TcpServer(object):
	pass


if __name__ == '__main__':
	pass
