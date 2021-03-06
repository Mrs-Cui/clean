#! /usr/bin/env python
# -*- coding:utf-8 -*-


# 简单工厂模式与 策略模式结合

class Discount(object):

    def __init__(self, discount):
        self.discount = discount

class Relief(object):

    def __int__(self, price_1, price_2):
        self.price_1 = price_1
        pass

class Context(object):

    def __init__(self, *args, **kwargs):
        pass

    def execute(self, *args, **kwargs):
        """
            代码执行
        :param args:
        :param kwargs:
        :return:
        """

# 抽象工厂模式

# 目的 业务逻辑与 数据访问的解偶
# 抽象工厂模式: 对多个产品抽象
class MainInfo(object):
    pass


class FirstMainInfo(MainInfo):
    pass

class SecondMainInfo(MainInfo):
    pass


# 简单工厂 + 抽象工厂
class DataBase(object):

    def __init__(self):
        pass

    def execute(self):

        if '':
            pass
        elif '':
            pass

# 反射 + 抽象工厂
class ReflexDataBase(object):
    pass




# 观察者模式

class FrontDesk(object):

    def __init__(self):
        self.status = -1
        self.family_people = []

    def add_people(self, oj):
        self.family_people.append(oj)

    def notify(self, message):
        for people in self.family_people:
            print(people.name, message)

class Colleague(object):

    def __init__(self, name, oj):
        self.name = name
        self.notify_oj = oj

    def work(self):
        print('开始工作')

# 实例模式

class Instance(object):

    def __init__(self):
        super(Instance, self).__init__()

    def __new__(cls, *args, **kwargs):
        return super(Instance, cls).__new__(*args, **kwargs)


# 单例模式

from threading import Lock, local

class Singleton(object):
    lock = Lock()
    _current = local()

    def __init__(self, *args, **kwargs):
        pass

    def make_current(self):
        self._current.instance = self

    def init(self):
        self.make_current()

    @classmethod
    def instance(cls):
        if not hasattr(Singleton._current, 'instance'):
            with Singleton.lock:
                Singleton._current.instance = Singleton()
        print(Singleton._current)
        return Singleton._current.instance

    def __new__(cls, *args, **kwargs):
        instance = super(Singleton, cls).__new__(cls)
        instance.init()
        return instance

# 策略模式
"""
    优点: 可以避免if else判断语句, 完美体现了`开闭原则`, 不用修改原有代码.
    缺点: 必须知道所有的策略.
"""

class Strategy(object):
    def __init__(self, strategy):
        print('bbbbb')


class StrategyA(Strategy):

    def __init__(self, strategy):
        super(StrategyA, self).__init__(strategy)


class StrategyB(Strategy):
    pass


class StrategyExecute(object):

    def __init__(self, strategy):
        print('aaaaaaaa')
        self.strategy = strategy

    def main(self):
        pass

    def __new__(cls, *args, **kwargs):
        strategy_cls = args[0]
        instance = super(StrategyExecute, cls).__new__(strategy_cls)
        return instance

# 代理模式


class RealSubject(object):

    def __new__(cls, *args, **kwargs):
        instance = super(RealSubject, cls).__new__(cls)
        return instance

    def execute(self):
        print('执行逻辑')


class Proxy(RealSubject):

    def __new__(cls, *args, **kwargs):
        instance = super(Proxy, cls).__new__(cls)
        return instance


class Client(object):

    def request(self):
        pass


# 观察者模式
"""
    被观察者的行为变化影响到观察者
"""


class Subject(object):

    def __init__(self):
        self.observer = []

    def add(self, observer):
        self.observer.append(observer)

    def execute(self):
        for observer in self.observer:
            pass


class Observer(object):
    pass


class RealObserverA(Observer):
    pass


class RealObserverB(Observer):
    pass

if __name__ == '__main__':
    execute = StrategyExecute(StrategyA)
    print(type(execute), type(StrategyA), type(StrategyA('a')))
