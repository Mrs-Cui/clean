#! /usr/bin/env python
# -*- coding:utf-8 -*-
import os
import requests
import time
from tornado.httpserver import HTTPServer, HTTPRequest
from tornado.ioloop import IOLoop
from tornado import netutil
from tornado import httputil
from tornado import concurrent
from tornado import web, gen, process, httpclient
from concurrent.futures import ThreadPoolExecutor


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


class NewHandleRequest(web.RequestHandler):
    executor = ThreadPoolExecutor(os.cpu_count() * 2)

    @gen.coroutine
    def get(self, *args, **kwargs):
        urls = ['https://www.baidu.com',] * 5
        print(urls)
        results = []
        start = time.time()
        for url in urls:
            request = httpclient.HTTPRequest(url=url)
            future = self.handle(request)
            results.append(future)
        for future in results:
            print(future.result())
        self.finish('hello world')
        print('spend time: ', time.time() - start)

    @gen.coroutine
    @web.asynchronous
    def post(self, *args, **kwargs):
        urls = ['https://www.baidu.com',] * 5
        results = []
        start = time.time()
        print(urls)
        client = httpclient.AsyncHTTPClient()

        for url in urls:
            request = httpclient.HTTPRequest(url=url)
            result = client.fetch(request, callback=self.finish_response)
            print('result', result)
            results.append(result)
        print('response results:', results)
        print('post spend time:', time.time() - start)

    def finish_response(self, response):
        self.finish('hello world')

    @concurrent.run_on_executor()
    def handle(self, request):
        response = requests.get(request.url)
        return response.content

if __name__ == '__main__':
    app = web.Application([
        (r'/handle_request', NewHandleRequest)
    ])
    sockets = netutil.bind_sockets(6666, reuse_port=True)
    process.fork_processes(os.cpu_count() * 2)
    server = NewHttpServer(app)
    server.add_sockets(sockets)
    IOLoop.current().start()
