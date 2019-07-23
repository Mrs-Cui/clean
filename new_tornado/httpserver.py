#! /usr/bin/env python
# -*- coding:utf-8 -*-

import typing
from typing import Any, Union, Dict, Callable, List, Type, Set, Tuple, Optional, Awaitable

from tornado import iostream, netutil
import ssl
import socket
from tornado.escape import native_str
from new_tornado.tcpserver import TcpServer
from new_tornado.util import Configurable
from new_tornado.httputil import HTTPServerConnectionDelegate
from tornado.simple_httpclient import HTTP1ConnectionParameters
from tornado.http1connection import HTTP1ServerConnection
from tornado import httputil
from tornado.httpserver import _ProxyAdapter

class _HTTPRequestContext(object):
	def __init__(
			self,
			stream: iostream.IOStream,
			address: Tuple,
			protocol: Optional[str],
			trusted_downstream: List[str] = None,
	) -> None:
		self.address = address
		# Save the socket's address family now so we know how to
		# interpret self.address even after the stream is closed
		# and its socket attribute replaced with None.
		if stream.socket is not None:
			self.address_family = stream.socket.family
		else:
			self.address_family = None
		# In HTTPServerRequest we want an IP, not a full socket address.
		if (
				self.address_family in (socket.AF_INET, socket.AF_INET6)
				and address is not None
		):
			self.remote_ip = address[0]
		else:
			# Unix (or other) socket; fake the remote address.
			self.remote_ip = "0.0.0.0"
		if protocol:
			self.protocol = protocol
		elif isinstance(stream, iostream.SSLIOStream):
			self.protocol = "https"
		else:
			self.protocol = "http"
		self._orig_remote_ip = self.remote_ip
		self._orig_protocol = self.protocol
		self.trusted_downstream = set(trusted_downstream or [])

	def __str__(self) -> str:
		if self.address_family in (socket.AF_INET, socket.AF_INET6):
			return self.remote_ip
		elif isinstance(self.address, bytes):
			# Python 3 with the -bb option warns about str(bytes),
			# so convert it explicitly.
			# Unix socket addresses are str on mac but bytes on linux.
			return native_str(self.address)
		else:
			return str(self.address)

	def _apply_xheaders(self, headers: httputil.HTTPHeaders) -> None:
		"""Rewrite the ``remote_ip`` and ``protocol`` fields."""
		# Squid uses X-Forwarded-For, others use X-Real-Ip
		ip = headers.get("X-Forwarded-For", self.remote_ip)
		# Skip trusted downstream hosts in X-Forwarded-For list
		for ip in (cand.strip() for cand in reversed(ip.split(","))):
			if ip not in self.trusted_downstream:
				break
		ip = headers.get("X-Real-Ip", ip)
		if netutil.is_valid_ip(ip):
			self.remote_ip = ip
		# AWS uses X-Forwarded-Proto
		proto_header = headers.get(
			"X-Scheme", headers.get("X-Forwarded-Proto", self.protocol)
		)
		if proto_header:
			# use only the last proto entry if there is more than one
			# TODO: support trusting mutiple layers of proxied protocol
			proto_header = proto_header.split(",")[-1].strip()
		if proto_header in ("http", "https"):
			self.protocol = proto_header

	def _unapply_xheaders(self) -> None:
		"""Undo changes from `_apply_xheaders`.

		Xheaders are per-request so they should not leak to the next
		request on the same connection.
		"""
		self.remote_ip = self._orig_remote_ip
		self.protocol = self._orig_protocol


class _CallableAdapter(httputil.HTTPMessageDelegate):
	def __init__(
			self,
			request_callback: Callable[[httputil.HTTPServerRequest], None],
			request_conn: httputil.HTTPConnection,
	) -> None:
		self.connection = request_conn
		self.request_callback = request_callback
		self.request = None  # type: Optional[httputil.HTTPServerRequest]
		self.delegate = None
		self._chunks = []  # type: List[bytes]

	def headers_received(
			self,
			start_line: Union[httputil.RequestStartLine, httputil.ResponseStartLine],
			headers: httputil.HTTPHeaders,
	) -> Optional[Awaitable[None]]:
		self.request = httputil.HTTPServerRequest(
			connection=self.connection,
			start_line=typing.cast(httputil.RequestStartLine, start_line),
			headers=headers,
		)
		return None

	def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
		self._chunks.append(chunk)
		return None

	def finish(self) -> None:
		assert self.request is not None
		self.request.body = b"".join(self._chunks)
		self.request._parse_body()
		self.request_callback(self.request)

	def on_connection_close(self) -> None:
		del self._chunks


class HttpServer(TcpServer, Configurable, HTTPServerConnectionDelegate):

	def __init__(self, *args: Any, **kwargs: Any) -> None:
		pass

	def initialize(
			self,
			request_callback: Union[
				httputil.HTTPServerConnectionDelegate,
				Callable[[httputil.HTTPServerRequest], None],
			],
			no_keep_alive: bool = False,
			xheaders: bool = False,
			ssl_options: Union[Dict[str, Any], ssl.SSLContext] = None,
			protocol: str = None,
			decompress_request: bool = False,
			chunk_size: int = None,
			max_header_size: int = None,
			idle_connection_timeout: float = None,
			body_timeout: float = None,
			max_body_size: int = None,
			max_buffer_size: int = None,
			trusted_downstream: List[str] = None,
	):
		self.request_callback = request_callback
		self.xheaders = xheaders
		self.protocol = protocol
		self.conn_params = HTTP1ConnectionParameters(
			decompress=decompress_request,
			chunk_size=chunk_size,
			max_header_size=max_header_size,
			header_timeout=idle_connection_timeout or 3600,
			max_body_size=max_body_size,
			body_timeout=body_timeout,
			no_keep_alive=no_keep_alive,
		)
		TcpServer.__init__(
			self,
			ssl_options=ssl_options,
			max_buffer_size=max_buffer_size,
			read_chunk_size=chunk_size,
		)
		self._connections = set()  # type: Set[HTTP1ServerConnection]
		self.trusted_downstream = trusted_downstream

	@classmethod
	def configurable_base(cls) -> Type[Configurable]:
		return HttpServer

	@classmethod
	def configurable_default(cls) -> Type[Configurable]:
		return HttpServer

	async def close_all_connections(self) -> None:
		"""Close all open connections and asynchronously wait for them to finish.

		This method is used in combination with `~.TCPServer.stop` to
		support clean shutdowns (especially for unittests). Typical
		usage would call ``stop()`` first to stop accepting new
		connections, then ``await close_all_connections()`` to wait for
		existing connections to finish.

		This method does not currently close open websocket connections.

		Note that this method is a coroutine and must be caled with ``await``.

		"""
		while self._connections:
			# Peek at an arbitrary element of the set
			conn = next(iter(self._connections))
			await conn.close()

	def handle_stream(self, stream: iostream.IOStream, address: Tuple) -> None:
		context = _HTTPRequestContext(
			stream, address, self.protocol, self.trusted_downstream
		)
		conn = HTTP1ServerConnection(stream, self.conn_params, context)
		self._connections.add(conn)
		conn.start_serving(self)

	def start_request(
			self, server_conn: object, request_conn: httputil.HTTPConnection
	) -> httputil.HTTPMessageDelegate:
		if isinstance(self.request_callback, httputil.HTTPServerConnectionDelegate):
			delegate = self.request_callback.start_request(server_conn, request_conn)
		else:
			delegate = _CallableAdapter(self.request_callback, request_conn)

		if self.xheaders:
			delegate = _ProxyAdapter(delegate, request_conn)

		return delegate

	def on_close(self, server_conn: object) -> None:
		self._connections.remove(typing.cast(HTTP1ServerConnection, server_conn))


if __name__ == '__main__':
	pass
