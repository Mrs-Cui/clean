#! /usr/bin/env python
# -*- coding:utf-8 -*-

class A(object):

	def __init__(self):
		pass

	def kill_people(cls):
		print(type(cls), cls)
		a = A()
		print(a)


if __name__ == '__main__':
	a = A()
	a.kill_people()