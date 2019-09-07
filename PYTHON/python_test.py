#! /usr/bin/env python
# -*- coding:utf-8 -*-

import requests

import webbrowser

from websocket import server
from websocket import WebSocket
class A(object):

	def __init__(self):
		pass

	def kill_people(self):
		print(self, type(self))
		a = A()
		print(a)

	@classmethod
	def life_people(cls):
		print(cls, type(cls))

	@staticmethod
	def hard_people():
		print('execute people')


class B(A):
	pass


import functools
def decorator1(funcs):
	print('start decorator1')
	@functools.wraps(funcs)
	def wrap(*args, **kwargs):
		print('exec decorator1')
		return funcs(*args, **kwargs)
	return wrap

def decorator2(funcs):
	print('start decorator2')
	@functools.wraps(funcs)
	def wrap(*args, **kwargs):
		print('exec decorator2')
		return funcs(*args, **kwargs)
	return wrap

@decorator2
@decorator1
def temp_a():
	print('hello world')
if __name__ == '__main__':
	temp_a()