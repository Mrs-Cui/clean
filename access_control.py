#! /usr/bin/env python
# -*- coding:utf-8 -*-

import abc
from abc import ABCMeta


class UserInfoAbc(ABCMeta):

    def check_password(self):
        pass

    def __new__(cls, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        pass


class AccessAbc(ABCMeta):
    pass


class DataAccess(AccessAbc):
    pass


class MenuAccess(AccessAbc):
    pass


class RolesAbc(ABCMeta):
    pass


class ManagerRoles(RolesAbc):
    pass


class TeamLeader(RolesAbc):
    pass


class OtherUser(UserInfoAbc):
    pass


class OtherAccess(AccessAbc):
    pass


class User(object):

    def __init__(self):
        self.a = 'a'

    # def __getattribute__(self, item):
    #
    #     return super(User, self).__getattribute__(item)

    def __getattr__(self, item):
        print(self.__getattr__.__name__)
        self.__dict__.get(item)

import os
import threading
r, w = os.pipe()
reader = os.fdopen(r, 'rb', 0)
writer = os.fdopen(w, 'wb', 0)

class Decorate(object):

    def __init__(self, func):
        self.func = func

    def decorate(self):
        pass

    def __call__(self, *args, **kwargs):
        print(self.func)

@Decorate
def decorate():
    pass


import pymysql
import csv
import json
def handel():
    conn = pymysql.connect(
        **{
            'host': 'vshow.ciegpdaw3vtl.eu-central-1.rds.amazonaws.com',
            'port': 3306,
            'db': 'social',
            'user': 'http',
            'passwd': 'boUnTNQm',
            'charset': 'utf8mb4',
            'autocommit': True
        }
    )
    sql = """
        select user.id as id from component.AnchorList as account left join social.user_info as user on
  user.id = substr(substring_index(account.jid, '@', 1), 8)
  where user.report_to = 'Mouhcine'
    """
    cursor = conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    results = [item[0] for item in results]
    print(len(results))
    sql = "update social.user_info set report_to = 'One' where id = %s"
    for item in results:
        print(item)
        cursor.execute(sql, (item, ))
    conn.commit()
from threading import local





if __name__ == '__main__':
    handel()

