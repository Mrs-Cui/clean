#! /usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from io import BytesIO
import tornado

from tornado import escape
from tornado import httputil
from tornado.log import access_log

from typing import List, Tuple, Optional, Callable, Any, Dict, Text
from types import TracebackType
import typing

def to_wsgi_str(s: bytes) -> str:
	assert isinstance(s, bytes)
	return s.decode("latin1")


class WSGIContainer(object):

	def __init__(self, wsgi_application: "WSGIAppType") -> None:

		self.wsgi_application = wsgi_application

	def __call__(self, request: httputil.HTTPServerRequest) -> None:
		data = dict()
		response = []

		def start_response(status: str, headers, exc_info):
			data["status"] = status
			data["headers"] = headers
			return response.append

		app_response = self.wsgi_application(
			WSGIContainer.environ(request), start_response
		)
		try:
			response.extend(app_response)
			body = b"".join(response)
		finally:
			if hasattr(app_response, "close"):
				app_response.close()  # type: ignore
		if not data:
			raise Exception("WSGI app did not call start_response")
		status_code_str, reason = data["status"].split(" ", 1)
		status_code = int(status_code_str)
		headers = data["headers"]  # type: List[Tuple[str, str]]
		header_set = set(k.lower() for (k, v) in headers)
		body = escape.utf8(body)
		if status_code != 304:
			if "content-length" not in header_set:
				headers.append(("Content-Length", str(len(body))))
			if "content-type" not in header_set:
				headers.append(("Content-Type", "text/html; charset=UTF-8"))
		if "server" not in header_set:
			headers.append(("Server", "TornadoServer/%s" % tornado.version))

		start_line = httputil.ResponseStartLine("HTTP/1.1", status_code, reason)
		header_obj = httputil.HTTPHeaders()
		for key, value in headers:
			header_obj.add(key, value)
		assert request.connection is not None
		request.connection.write_headers(start_line, header_obj, chunk=body)
		request.connection.finish()
		self._log(status_code, request)

	@staticmethod
	def environ(request: httputil.HTTPServerRequest) -> Dict[Text, Any]:
		"""Converts a `tornado.httputil.HTTPServerRequest` to a WSGI environment.
		"""
		hostport = request.host.split(":")
		if len(hostport) == 2:
			host = hostport[0]
			port = int(hostport[1])
		else:
			host = request.host
			port = 443 if request.protocol == "https" else 80
		environ = {
			"REQUEST_METHOD": request.method,
			"SCRIPT_NAME": "",
			"PATH_INFO": to_wsgi_str(
				escape.url_unescape(request.path, encoding=None, plus=False)
			),
			"QUERY_STRING": request.query,
			"REMOTE_ADDR": request.remote_ip,
			"SERVER_NAME": host,
			"SERVER_PORT": str(port),
			"SERVER_PROTOCOL": request.version,
			"wsgi.version": (1, 0),
			"wsgi.url_scheme": request.protocol,
			"wsgi.input": BytesIO(escape.utf8(request.body)),
			"wsgi.errors": sys.stderr,
			"wsgi.multithread": False,
			"wsgi.multiprocess": True,
			"wsgi.run_once": False,
		}
		if "Content-Type" in request.headers:
			environ["CONTENT_TYPE"] = request.headers.pop("Content-Type")
		if "Content-Length" in request.headers:
			environ["CONTENT_LENGTH"] = request.headers.pop("Content-Length")
		for key, value in request.headers.items():
			environ["HTTP_" + key.replace("-", "_").upper()] = value
		return environ

	def _log(self, status_code: int, request: httputil.HTTPServerRequest) -> None:
		if status_code < 400:
			log_method = access_log.info
		elif status_code < 500:
			log_method = access_log.warning
		else:
			log_method = access_log.error
		request_time = 1000.0 * request.request_time()
		assert request.method is not None
		assert request.uri is not None
		summary = request.method + " " + request.uri + " (" + request.remote_ip + ")"
		log_method("%d %s %.2fms", status_code, summary, request_time)


HTTPRequest = httputil.HTTPServerRequest

if __name__ == '__main__':
	pass