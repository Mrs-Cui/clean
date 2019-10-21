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
    print('gen', num)
    yield 2
    yield 3
    return 4


def test01(gen):
    while True:
        ll = yield from gen()
        gen().close()
        print('proxy', ll)


def run_main():
    gen = test01(generator01)
    print(type(gen), gen.__str__())
    print(gen.send(None))
    print(gen.send(101))
    # print(gen.throw(ValueError))
    print(gen.send(None))
    print(gen.send(None))
    # gen.throw(StopIteration)
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


final_result = {}


def sales_sum(pro_name):
    total = 0
    nums = []
    while True:
        x = yield
        print(pro_name + '销量', x)
        if not x:
            break
        total += x
        nums.append(x)
    return total, nums  # 程序运行到return的时候，会将return的返回值返回给委托方，即middle中的final_result[key]


def middle(key):
    while True:  # 相当于不停监听sales_sum是否有返回数据，（本例中有三次返回）
        final_result[key] = yield from sales_sum(key)
        print(key + '销量统计完成！！')


def main_2():
    data_sets = {
        '面膜': [1200, 1500, 3000],
        '手机': [88, 100, 98, 108],
        '衣服': [280, 560, 778, 70],
    }

    for key, data_set in data_sets.items():
        print('start key', key)
        m = middle(key)
        m.send(None)  # 预激生成器
        for value in data_set:
            m.send(value)
        m.send(None)  # 发送一个None使sales_sum中的x值为None退出while循环

    print(final_result)


if __name__ == "__main__":
    run_main()
