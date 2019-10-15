#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import fcntl
import select
from multiprocessing import Process, Pool

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




def multi_process():
	children = {}
	def create_subprocess(i):
		pid = os.fork()
		if pid == 0:
			print('子进程:', i, os.getpid(), os.getppid())
		else:
			print('父进程', i, os.getpid(), os.getppid())
		children[pid] = i
		return pid
	process_num = os.cpu_count()
	for i in range(3):
		pid = create_subprocess(i)
		if pid == 0:
			return
	print(children)
	while children:
		pid, statue = os.wait()
	print(os.getpid(), '多进程结束')

def target_func(target_name):
	print(target_name)

def multi_process_exec():
	task_pool = Pool(os.cpu_count())
	for i in range(10):
		task_pool.apply_async(target_func, args=('process name: %s' % (i), ))
	task_pool.close()
	task_pool.join()
	print('并发结束')



def os_pipe():
	r, w = os.pipe()
	pid = os.fork()
	if pid != 0:
		reader = os.fdopen(r)
		os.close(w)
		print('parent process read!')
		str = reader.read()
		print('text: ', str)
		sys.exit(0)
	else:
		os.close(r)
		writer = os.fdopen(w, 'w')
		print('child process, write!')
		writer.write('hello world')
		writer.close()
		sys.exit(0)

def fcntl_fd():
	fd = open('../note_book', 'r')
	print(fd)
	flags = fcntl.fcntl(fd, fcntl.F_GETFD)
	print(flags)
	fcntl.fcntl(fd, fcntl.F_SETFD, flags | fcntl.FD_CLOEXEC)
	print(fd.__class__)

def select_epoll():
	epoll = select.epoll()
	print(epoll.poll(10))
if __name__ == '__main__':
	select_epoll()
