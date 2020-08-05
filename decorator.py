#! /usr/bin/env python
#-*-coding:utf-8-*-

def decorator_book(cls):
    cls._state = dict()
    origin_init = cls.__init__
    def new_init(self, *args, **kwargs):
        self.__dict__ = cls._state
        origin_init(self, *args, **kwargs)
    cls.__init__ = new_init
    return cls

@decorator_book
class Book(object):

    def __init__(self, name):
        self.name = name


if __name__ == '__main__':
    b = Book('狼人杀')
    c = Book('千人杀')
    print(b.name)
    print(c.name)
    b.d = '完了'
    print(c.d)