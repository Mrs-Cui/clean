#! /usr/bin/env python
# -*- coding:utf-8 -*-

# from __future__ import all_feature_names

import asyncio
import contextvars
import time
from threading import local
import sys
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

if __name__ == '__main__':
	pool = ThreadPoolExecutor(100)

	results = []
	for i in range(100):
		result = pool.submit(contextvars_clean, i)
		results.append(result)
	pool.shutdown()
	for pos, result in enumerate(results):
		print(pos, result.result())