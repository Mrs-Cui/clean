#! /usr/bin/env python
# -*- coding:utf-8 -*-

from tornado import ioloop
from tornado import httpserver

from new_tornado.wsgi import WSGIContainer

def simple_app(environ, start_response):
	status = "200 OK"
	response_headers = [("Content-type", "text/plain")]
	start_response(status, response_headers)
	return ["Hello world!\n"]


if __name__ == '__main__':
	print('start !!!!')
	container = WSGIContainer(simple_app)
	server = httpserver.HTTPServer(container)
	server.bind(8888)
	ioloop.IOLoop.current().start()
	print('end !!!!')