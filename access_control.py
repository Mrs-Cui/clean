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
            'db': 'thirdpartyunion',
            'user': 'http',
            'passwd': 'boUnTNQm',
            'charset': 'utf8mb4'
        }
    )
    sql = """
        update thirdpartyunion.account_userextra set country=%s, first_language=%s,
        second_language=%s, third_language=%s, service_language=%s where belong=%s and report_to=%s
    """
    cursor = conn.cursor()
    with open('handle_1.csv', 'r') as file:
        reader = csv.DictReader(file, fieldnames=[
            'belong to', 'report to', 'country', 'first', 'second', 'third'
        ])
        results = []
        for row in reader:
            service_language = [i.strip() for i in [row['first'], row['second'], row['third']] if i.strip() != '/']
            if row['third'].strip() == '/':
                row['third'] = ''
            results.append([
                row['country'], row['first'].strip(), row['second'].strip(), row['third'].strip(),
                json.dumps(service_language), row['belong to'].strip(), row['report to'].strip()
            ])
    print(results)
    cursor.executemany(sql, results)
    conn.commit()

if __name__ == '__main__':
    handel()
