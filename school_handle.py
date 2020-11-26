#! /usr/bin/env python
# -*- coding:utf-8 -*-

"""
    北京中学信息爬取
"""
import csv
import requests
import pymongo
from gevent.pool import Pool
import json
import re
from copy import deepcopy
from lxml import etree
import sys

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'Host': 'map.beijing.gov.cn'
}

connect = pymongo.MongoClient('127.0.0.1', 27017)

def run(start_url):
    task_pool = Pool(20)

    headers = deepcopy(HEADERS)
    headers['X-Requested-With'] = 'XMLHttpRequest'
    response = requests.get(url=start_url, headers=HEADERS)
    content = response.content
    region_info = json.loads(str(content, encoding='utf-8'))
    base_url = 'https://map.beijing.gov.cn/api/place_list_for_category.json?categoryId=zx&regionId={0}'
    for region in region_info:
        url = base_url.format(region['regionId'])
        task_pool.apply_async(region_handle, args=(url, headers))
    task_pool.join()


def region_handle(url, headers):
    response = requests.get(url=url, headers=headers)
    data = json.loads(str(response.content, encoding='utf-8'))
    school_handle(data)


def school_handle(schools):
    task_pool = Pool(20)
    for school in schools:
        task_pool.apply_async(school_detail_handle, args=(school,))
    task_pool.join()

def school_detail_handle(school):
    print(school)
    base_url = 'https://map.beijing.gov.cn/place?placeId={0}&categoryId=zx'
    url = base_url.format(school['placeId'])
    response = requests.get(url, headers=HEADERS)
    content = response.content
    html = etree.HTML(content)
    tr = html.xpath('//table//tr[last()]')
    text = tr[0].xpath('./td/text()')
    if text:
        content = text[0]
        nature = re.search(r'性质：(.*?)(?=\()', content)
        school_section = re.search(r'学段：(.*?)(?=\()', content)
        school_size = re.search(r'学校规模：(.*?)(?=\()', content)
        if nature:
            school['nature'] = nature.group()
        if school_section:
            school['school_section'] = school_section.group()
        if school_size:
            school['school_size'] = school_size.group()
    connect['Data']['School'].insert(school)




if __name__ == '__main__':
    run("https://map.beijing.gov.cn/api/district_list_for_category.json?categoryId=zx")
    # school_detail_handle({'placeId': '5ba765b97e4e7316d93853ae'})
