#! /usr/bin/env python
# -*- coding:utf-8 -*-

# from __future__ import all_feature_names

import asyncio
import contextvars
import time
from threading import local
import sys
from copy import copy, deepcopy
from concurrent.futures import ThreadPoolExecutor
import dataclasses
context = contextvars.ContextVar('var', default=-1)


def contextvars_clean(i):
	context.set(i)
	time.sleep(1)
	return context.get()

@dataclasses.dataclass(init=True,eq=True, order=True,repr=True)
class Field(object):

	pass

class greenlet(object):
	def __bool__(self, *args, **kwargs):  # real signature unknown
		""" self != 0 """
		pass

	def __getstate__(self, *args, **kwargs):  # real signature unknown
		pass

	def __init__(self, run=None, parent=None):  # real signature unknown; restored from __doc__
		pass



	dead = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

	gr_frame = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

	parent = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

	run = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

	_stack_saved = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

	error = 'Error'
	GreenletExit = None  # (!) forward: GreenletExit, real value is "<class 'greenlet.GreenletExit'>"
	__dict__ = None  # (!) real value is "mappingproxy({'__init__': <slot wrapper '__init__' of 'greenlet.greenlet' objects>, '__bool__': <slot wrapper '__bool__' of 'greenlet.greenlet' objects>, '__new__': <built-in method __new__ of type object at 0x7f799fa80d20>, 'switch': <method 'switch' of 'greenlet.greenlet' objects>, 'throw': <method 'throw' of 'greenlet.greenlet' objects>, '__getstate__': <method '__getstate__' of 'greenlet.greenlet' objects>, '__dict__': <attribute '__dict__' of 'greenlet.greenlet' objects>, 'run': <attribute 'run' of 'greenlet.greenlet' objects>, 'parent': <attribute 'parent' of 'greenlet.greenlet' objects>, 'gr_frame': <attribute 'gr_frame' of 'greenlet.greenlet' objects>, 'dead': <attribute 'dead' of 'greenlet.greenlet' objects>, '_stack_saved': <attribute '_stack_saved' of 'greenlet.greenlet' objects>, '__doc__': 'greenlet(run=None, parent=None) -> greenlet\\n\\nCreates a new greenlet object (without running it).\\n\\n - *run* -- The callable to invoke.\\n - *parent* -- The parent greenlet. The default is the current greenlet.', 'getcurrent': <built-in function getcurrent>, 'error': <class 'greenlet.error'>, 'GreenletExit': <class 'greenlet.GreenletExit'>, 'settrace': <built-in function settrace>, 'gettrace': <built-in function gettrace>})"


class Greenlet(greenlet):
	@property
	def loop(self):
		# needed by killall
		return self.parent

if __name__ == '__main__':
	pool = ThreadPoolExecutor(100)

	a = Greenlet()
	print(a.loop, dir(a.parent))
