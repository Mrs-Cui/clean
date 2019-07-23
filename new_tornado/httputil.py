#! /usr/bin/env python
# -*- coding:utf-8 -*-

import typing

from typing import Optional, Union, Awaitable, List, Mapping, Tuple, Deque, Iterable, Iterator
import collections
import calendar
import collections
import copy
import datetime
import email.utils
from http.client import responses
import http.cookies
import re
from ssl import SSLError
import time
import unicodedata
from urllib.parse import urlencode, urlparse, urlunparse, parse_qsl

from tornado.escape import native_str, parse_qs_bytes, utf8
from tornado.log import gen_log
from tornado.util import ObjectDict, unicode_type

_CRLF_RE = re.compile(r"\r?\n")


class HTTPInputError(Exception):
	pass


class _NormalizedHeaderCache(dict):
	"""Dynamic cached mapping of header names to Http-Header-Case.

	Implemented as a dict subclass so that cache hits are as fast as a
	normal dict lookup, without the overhead of a python function
	call.

	>>> normalized_headers = _NormalizedHeaderCache(10)
	>>> normalized_headers["coNtent-TYPE"]
	'Content-Type'
	"""

	def __init__(self, size: int) -> None:
		super(_NormalizedHeaderCache, self).__init__()
		self.size = size
		self.queue = collections.deque()  # type: Deque[str]

	def __missing__(self, key: str) -> str:
		normalized = "-".join([w.capitalize() for w in key.split("-")])
		self[key] = normalized
		self.queue.append(key)
		if len(self.queue) > self.size:
			# Limit the size of the cache.  LRU would be better, but this
			# simpler approach should be fine.  In Python 2.7+ we could
			# use OrderedDict (or in 3.2+, @functools.lru_cache).
			old_key = self.queue.popleft()
			del self[old_key]
		return normalized


_normalized_headers = _NormalizedHeaderCache(1000)


class HTTPHeaders(collections.abc.MutableMapping):

	@typing.overload
	def __init__(self, __arg: Mapping[str, List[str]]) -> None:
		pass

	@typing.overload  # noqa: F811
	def __init__(self, __arg: Mapping[str, str]) -> None:
		pass

	@typing.overload  # noqa: F811
	def __init__(self, *args: Tuple[str, str]) -> None:
		pass

	@typing.overload  # noqa: F811
	def __init__(self, **kwargs: str) -> None:
		pass

	def __init__(self, *args: typing.Any, **kwargs: str) -> None:  # noqa: F811
		self._dict = {}  # type: typing.Dict[str, str]
		self._as_list = {}  # type: typing.Dict[str, typing.List[str]]
		self._last_key = None
		if len(args) == 1 and len(kwargs) == 0 and isinstance(args[0], HTTPHeaders):
			# Copy constructor
			for k, v in args[0].get_all():
				self.add(k, v)
		else:
			# Dict-style initialization
			self.update(*args, **kwargs)

	# new public methods

	def add(self, name: str, value: str) -> None:
		"""Adds a new value for the given key."""
		norm_name = _normalized_headers[name]
		self._last_key = norm_name
		if norm_name in self:
			self._dict[norm_name] = (
					native_str(self[norm_name]) + "," + native_str(value)
			)
			self._as_list[norm_name].append(value)
		else:
			self[norm_name] = value

	def get_list(self, name: str) -> List[str]:
		"""Returns all values for the given header as a list."""
		norm_name = _normalized_headers[name]
		return self._as_list.get(norm_name, [])

	def get_all(self) -> Iterable[Tuple[str, str]]:
		"""Returns an iterable of all (name, value) pairs.

		If a header has multiple values, multiple pairs will be
		returned with the same name.
		"""
		for name, values in self._as_list.items():
			for value in values:
				yield (name, value)

	def parse_line(self, line: str) -> None:
		"""Updates the dictionary with a single header line.

		>>> h = HTTPHeaders()
		>>> h.parse_line("Content-Type: text/html")
		>>> h.get('content-type')
		'text/html'
		"""
		if line[0].isspace():
			# continuation of a multi-line header
			if self._last_key is None:
				raise HTTPInputError("first header line cannot start with whitespace")
			new_part = " " + line.lstrip()
			self._as_list[self._last_key][-1] += new_part
			self._dict[self._last_key] += new_part
		else:
			try:
				name, value = line.split(":", 1)
			except ValueError:
				raise HTTPInputError("no colon in header line")
			self.add(name, value.strip())

	@classmethod
	def parse(cls, headers: str) -> "HTTPHeaders":
		"""Returns a dictionary from HTTP header text.

		>>> h = HTTPHeaders.parse("Content-Type: text/html\\r\\nContent-Length: 42\\r\\n")
		>>> sorted(h.items())
		[('Content-Length', '42'), ('Content-Type', 'text/html')]

		.. versionchanged:: 5.1

		   Raises `HTTPInputError` on malformed headers instead of a
		   mix of `KeyError`, and `ValueError`.

		"""
		h = cls()
		for line in _CRLF_RE.split(headers):
			if line:
				h.parse_line(line)
		return h

	# MutableMapping abstract method implementations.

	def __setitem__(self, name: str, value: str) -> None:
		norm_name = _normalized_headers[name]
		self._dict[norm_name] = value
		self._as_list[norm_name] = [value]

	def __getitem__(self, name: str) -> str:
		return self._dict[_normalized_headers[name]]

	def __delitem__(self, name: str) -> None:
		norm_name = _normalized_headers[name]
		del self._dict[norm_name]
		del self._as_list[norm_name]

	def __len__(self) -> int:
		return len(self._dict)

	def __iter__(self) -> Iterator[typing.Any]:
		return iter(self._dict)

	def copy(self) -> "HTTPHeaders":
		# defined in dict but not in MutableMapping.
		return HTTPHeaders(self)

	# Use our overridden copy method for the copy.copy module.
	# This makes shallow copies one level deeper, but preserves
	# the appearance that HTTPHeaders is a single container.
	__copy__ = copy

	def __str__(self) -> str:
		lines = []
		for name, value in self.get_all():
			lines.append("%s: %s\n" % (name, value))
		return "".join(lines)

	__unicode__ = __str__


class HTTPServerConnectionDelegate(object):
	"""Implement this interface to handle requests from `.HTTPServer`.

	.. versionadded:: 4.0
	"""

	def start_request(
			self, server_conn: object, request_conn: "HTTPConnection"
	) -> "HTTPMessageDelegate":
		"""This method is called by the server when a new request has started.

		:arg server_conn: is an opaque object representing the long-lived
			(e.g. tcp-level) connection.
		:arg request_conn: is a `.HTTPConnection` object for a single
			request/response exchange.

		This method should return a `.HTTPMessageDelegate`.
		"""
		raise NotImplementedError()

	def on_close(self, server_conn: object) -> None:
		"""This method is called when a connection has been closed.

		:arg server_conn: is a server connection that has previously been
			passed to ``start_request``.
		"""
		pass


class HTTPMessageDelegate(object):
	"""Implement this interface to handle an HTTP request or response.

	.. versionadded:: 4.0
	"""

	# TODO: genericize this class to avoid exposing the Union.
	def headers_received(
			self,
			start_line: Union["RequestStartLine", "ResponseStartLine"],
			headers: HTTPHeaders,
	) -> Optional[Awaitable[None]]:
		"""Called when the HTTP headers have been received and parsed.

		:arg start_line: a `.RequestStartLine` or `.ResponseStartLine`
			depending on whether this is a client or server message.
		:arg headers: a `.HTTPHeaders` instance.

		Some `.HTTPConnection` methods can only be called during
		``headers_received``.

		May return a `.Future`; if it does the body will not be read
		until it is done.
		"""
		pass

	def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
		"""Called when a chunk of data has been received.

		May return a `.Future` for flow control.
		"""
		pass

	def finish(self) -> None:
		"""Called after the last chunk of data has been received."""
		pass

	def on_connection_close(self) -> None:
		"""Called if the connection is closed without finishing the request.

		If ``headers_received`` is called, either ``finish`` or
		``on_connection_close`` will be called, but not both.
		"""
		pass


class HttpServerRequest(object):
	pass
