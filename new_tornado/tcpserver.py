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

	def __init__(
			self,
			ssl_options: Union[Dict[str, Any], ssl.SSLContext] = None,
			max_buffer_size: int = None,
			read_chunk_size: int = None,
	) -> None:
		self.ssl_options = ssl_options
		self._sockets = {}  # type: Dict[int, socket.socket]
		self._handlers = {}  # type: Dict[int, Callable[[], None]]
		self._pending_sockets = []  # type: List[socket.socket]
		self._started = False
		self._stopped = False
		self.max_buffer_size = max_buffer_size
		self.read_chunk_size = read_chunk_size

		if self.ssl_options is not None and isinstance(self.ssl_options, dict):
			# Only certfile is required: it can contain both keys
			if "certfile" not in self.ssl_options:
				raise KeyError('missing key "certfile" in ssl_options')

			if not os.path.exists(self.ssl_options["certfile"]):
				raise ValueError(
					'certfile "%s" does not exist' % self.ssl_options["certfile"]
				)
			if "keyfile" in self.ssl_options and not os.path.exists(
					self.ssl_options["keyfile"]
			):
				raise ValueError(
					'keyfile "%s" does not exist' % self.ssl_options["keyfile"]
				)

	def listen(self, port: int, address: str = '') -> None:
		sockets = bind_sockets(port, address=address)
		self.add_sockets(sockets)

	def add_sockets(self, sockets: List[socket.socket]):

		for sock in sockets:
			self._sockets[sock.fileno()] = sock
			self._handlers[sock.fileno()] = add_accept_handler(
				sock, self._handle_connection
			)

	def _handle_connection(self, connection: socket.socket, address: Any) -> None:
		if self.ssl_options is not None:
			assert ssl, "Python 2.6+ and OpenSSL required for SSL"
			try:
				connection = ssl_wrap_socket(
					connection,
					self.ssl_options,
					server_side=True,
					do_handshake_on_connect=False,
				)
			except ssl.SSLError as err:
				if err.args[0] == ssl.SSL_ERROR_EOF:
					return connection.close()
				else:
					raise
			except socket.error as err:
				if errno_from_exception(err) in (errno.ECONNABORTED, errno.EINVAL):
					return connection.close()
				else:
					raise
		try:
			if self.ssl_options is not None:
				stream = SSLIOStream(
					connection,
					max_buffer_size=self.max_buffer_size,
					read_chunk_size=self.read_chunk_size,
				)  # type: IOStream
			else:
				stream = IOStream(
					connection,
					max_buffer_size=self.max_buffer_size,
					read_chunk_size=self.read_chunk_size,
				)

			future = self.handle_stream(stream, address)
			if future is not None:
				IOLoop.current().add_future(
					gen.convert_yielded(future), lambda f: f.result()
				)
		except Exception:
			app_log.error("Error in connection callback", exc_info=True)

	def handle_stream(self, stream: IOStream, address: tuple):

		raise NotImplementedError()
if __name__ == '__main__':
	pass
