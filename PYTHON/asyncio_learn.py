#! /usr/bin/env python
# -*- coding:utf-8 -*-

import asyncio
import time


async def say_after(delay, what):
	await asyncio.sleep(delay)
	print(what)


async def main():
	print(f"started at {time.strftime('%X')}")

	await say_after(1, 'hello')
	await say_after(2, 'world')

	print(f"finished at {time.strftime('%X')}")


async def main_1():
	task1 = asyncio.create_task(
		say_after(1, 'hello'))

	task2 = asyncio.create_task(
		say_after(2, 'world'))

	print(f"started at {time.strftime('%X')}")

	# Wait until both tasks are completed (should take
	# around 2 seconds.)
	await task1
	await task2

	print(f"finished at {time.strftime('%X')}")


async def clear():
	yield 'a'


def generator3():
	num = yield 1

	print(num)
	try:
		yield 2
	except ValueError:
		print("捕获异常：ValueError")
	yield 3


def run_generator3():
	gen = generator3()
	print(gen.send(None))
	print(gen.send(101))
	print(gen.send(None))
	gen.throw(ValueError)
	gen.close()


def generator01():
	num = yield 1
	print(num)
	yield 2
	yield 3
	return 4


def test01(gen):
	ll = yield from gen()
	print(ll)


def run_main():
	gen = test01(generator01)
	print(gen.send(None))
	print(gen.send(101))
	# print(gen.throw(ValueError))
	print(gen.send(None))
	print(gen.send(None))


import requests


async def request(url):
	return requests.get(url, proxies={'http': 'socks5://192.168.2.244:9091',
									  'https': 'socks5://192.168.2.244:9091'})


async def spider(url):
	return await request(url)


def run_spider():
	sp = spider("http://www.baidu.com", )
	print(asyncio.run(spider("http://www.baidu.com")))
	try:
		print(sp.send(None))
	except StopIteration as e:
		print(e.value)


async def factorial(name, number):
	f = 1
	for i in range(2, number + 1):
		print(f"Task {name}: Compute factorial({i})...")
		await asyncio.sleep(1)
		f *= i
	print(f"Task {name}: factorial({number}) = {f}")
	return name

async def run_factorial():
	# Schedule three calls *concurrently*:
	return await asyncio.gather(
		factorial("A", 2),
		factorial("B", 3),
		factorial("C", 4),
	)


if __name__ == "__main__":
	results = asyncio.run(run_factorial())
	print(results)
