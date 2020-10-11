#! /usr/bin/env python
# -*- coding:utf-8 -*-

#! /usr/bin/env python
# -*- coding:utf-8 -*-
import json

from scrapy import Spider, Request
from scrapy.responsetypes import Response
from scrapy.selector import SelectorList
from urllib import parse

import pymysql

MYSQL_CONFIG = {
    'host': 'vshow-storage.cbs7pdixzhmi.rds.cn-north-1.amazonaws.com.cn',
    'user': 'root',
    'password': 'k5p8uLRE',
    'db': 'commodity',
    'charset': 'utf8'
}

HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
}

SOURCE_URL = 'https://www.amazon.in'


class CommodityList(Spider):
    name = 'commodity_detail'
    conn = pymysql.connect(**MYSQL_CONFIG)

    def start_requests(self):
        urls = self.query_urls()
        for items in urls:
            commodity_amazonid, url = items
            url = url.split('ref')[0]
            if 'picassoRedirect' in url:
                continue
            url = url.replace('www.amazon.in//', 'www.amazon.in/')
            yield Request(url=url, callback=self.parse_book, cb_kwargs={'commodity_amazonid': commodity_amazonid}, headers=HEADERS)

    def query_urls(self):
        cursor = self.conn.cursor()
        sql = """
            select distinct commodity_amazonid, commodity_link from commodity.commodity_list where commodity_type = 'Books';
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        return results

    def parse_book(self, response, **kwargs):
        print(response.url)
        span = response.xpath('//span[@id="productSubtitle"]/text()')
        if span:
            book_name = span[0].get().strip('\n')
        else:
            return
        span = response.xpath('//span[@id="productSubtitle"]/text()')
        if span:
            book_sub_name = span[0].get().strip('\n')
        else:
            book_sub_name = ''
        a = response.xpath('//a[@data-asin]')
        if a:
            if a[0].attrib.get('data-asin'):
                anchor_name = a[0].xpath('./text()')[0].get()
                anchor_link = SOURCE_URL + a[0].xpath('./@href')[0].get()
            else:
                return
        else:
            return
        div = response.xpath('//noscript/div//p/text()|//noscript/div/text()')
        if div:
            book_introduce = '\n'.join([i.get() for i in div])
        else:
            book_introduce = ''
        li_list = response.xpath('//div[@id="detailBullets_feature_div"]/ul/li/span')
        book_detail = {}
        for li in li_list:
            span_list = li.xpath('./span')
            key = span_list[0].xpath('./text()')[0].get()
            value = span_list[1].xpath('./text()')[0].get()
            book_detail[key.strip('\n').strip(':').strip('\n')] = value.strip('')
        book_detail = json.dumps(book_detail)
        commodity_amazonid = kwargs.get('commodity_amazonid')
        img_list = response.xpath('//div[@id="imageBlockThumbs"]//img/@src')
        img_link = '|'.join([i.get() for i in img_list])
        print([
            commodity_amazonid, book_name, book_sub_name, anchor_name, anchor_link, book_detail, book_introduce
        ])
        result = [
            commodity_amazonid, book_name, book_sub_name, anchor_name, anchor_link, book_detail, book_introduce, img_link
        ]
        self.insert_data(result)

    def insert_data(self, results):
        cursor = self.conn.cursor()
        sql = """
            insert into commodity.books(commodity_amazonid, book_name, book_sub_name, anchor_name,
            anchor_link, book_detail, book_introduction, book_image_link
            ) values(%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, results)
        self.conn.commit()
        cursor.close()
