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
            print people.name, message

class Colleague(object):

    def __init__(self, name, oj):
        self.name = name
        self.notify_oj = oj

    def work(self):
        print '开始工作'

# 实例模式

class Instance(object):

    def __init__(self):
        super(Instance, self).__init__()

    def __new__(cls, *args, **kwargs):
        return super(Instance, cls).__new__(*args, **kwargs)
if __name__ == '__main__':
    pass
