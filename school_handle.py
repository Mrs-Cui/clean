#! /usr/bin/env python
# -*- coding:utf-8 -*-

"""
    北京中学信息爬取
"""
import csv
import requests
from gevent.pool import Pool
import json
import re
from copy import deepcopy
from lxml import etree
import sys
reload(sys)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'Host': 'map.beijing.gov.cn'
}

def run(start_url):
    headers = deepcopy(HEADERS)
    headers['X-Requested-With'] = 'XMLHttpRequest'
    response = requests.get(url=start_url, headers=HEADERS)
    content = response.content
    region_info = json.loads(content)
    base_url = 'https://map.beijing.gov.cn/api/place_list_for_category.json?categoryId=zx&regionId={0}'
    for region in region_info:
        url = base_url.format(region['regionId'])
        print(region)
        response = requests.get(url=url, headers=headers)
        data = json.loads(response.content)
        school_handle(data)


def school_handle(schools):
    task_pool = Pool(20)
    for school in schools:
        task_pool.apply_async(school_detail_handle, args=(school,))
    task_pool.join()

def school_detail_handle(school):
    base_url = 'https://map.beijing.gov.cn/place?placeId={0}&categoryId=zx'

    url = base_url.format(school['placeId'])
    response = requests.get(url, headers=HEADERS)
    content = response.content
    html = etree.HTML(content)
    tr = html.xpath('//table//tr[last()]')
    text = tr[0].xpath('./td/text()')
    if text:
        content = text[0]
        pattern = re.search(u'\u5b66\u6821\u89c4\u6a21(.*?)\(', content)
        if pattern:
            content = pattern.group(1)
        else:
            content = ''
    print(school['placeName'].encode('utf-8'))
    print(content.encode('utf-8'))
    write_to_csv((school['placeName'].encode('utf-8'), content.encode('utf-8').strip('：').strip('"')))

def write_to_csv(results):
    with open('/data/school.csv', 'a+') as file:
        writer = csv.writer(file)
        writer.writerow(results)




if __name__ == '__main__':
    run("https://map.beijing.gov.cn/api/district_list_for_category.json?categoryId=zx")
    # 
