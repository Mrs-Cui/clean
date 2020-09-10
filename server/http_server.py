#! /usr/bin/env python
# -*- coding:utf-8 -*-
import os

from tornado.httpserver import HTTPServer, HTTPRequest
from tornado.ioloop import IOLoop
from tornado import netutil
from tornado import httputil
from tornado import concurrent
from tornado import web, gen, process, httpclient


class NewHttpServer(HTTPServer):

    def handle_stream(self, stream, address):
        if self.ssl_options is not None:
            stream.wait_for_handshake()
        super(NewHttpServer, self).handle_stream(stream, address)


class HandleRequest(web.RequestHandler):

    @concurrent.run_on_executor
    def get(self, *args, **kwargs):

        async_client = httpclient.AsyncHTTPClient()
        request = self.handle_header(self.request)

        future = async_client.fetch(request, callback=self.request_callback)

    def post(self, *args, **kwargs):
        pass

    def handle_header(self, response):
        url = ''
        request = httpclient.HTTPRequest(url=url)
        return request

    def request_callback(self, response):
        self.finish()

if __name__ == '__main__':
    app = web.Application([
        (r'/handle_request', HandleRequest)
    ])
    sockets = netutil.bind_sockets(6666, reuse_port=True)
    process.fork_processes(os.cpu_count() * 2)
    server = NewHttpServer(app)
    server.add_sockets(sockets)
    IOLoop.current().start()
