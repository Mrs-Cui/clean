#! /usr/bin/env python
# -*- coding:utf-8 -*-

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

SOURCE_URL = 'https://www.amazon.in/'


class CommodityList(Spider):
    name = 'commodity_list'
    conn = pymysql.connect(**MYSQL_CONFIG)

    def start_requests(self):
        urls = [
            'https://www.amazon.in/'
        ]
        for url in urls:
            yield Request(url=url, callback=self.parse_class, cb_kwargs={'page': 100})

    def parse_class(self, response, **kwargs):
        options = response.xpath('//select[@id="searchDropdownBox"]/option')
        base_url = 'https://www.amazon.in/s?ref=nb_sb_noss_1&{params}'
        for option in options:
            content = option.xpath('./text()').get()
            value = option.attrib.get('value')
            if not value:
                continue
            if 'Books' in content:
                callback = self.parse_book
            else:
                continue
                # callback = self.parse_list
            for i in range(kwargs.get('page', 100)):
                url = base_url.format(params=parse.urlencode({'url': value, 'k': content, 'page': i}))
                yield Request(url=url, callback=callback, cb_kwargs={'category': content}, headers=HEADERS)

    def parse_images(self, div):
        images_list = []
        images = div.xpath('.//img[@class="s-image"]')
        for image in images:
            if image.attrib.get('src'):
                images_list.append(image.attrib.get('src', '').strip())
            if image.attrib.get('srcset'):
                srcset_list = image.attrib.get('srcset', '').split(',')
                for src in srcset_list:
                    images_list.append(src.strip().split(' ')[0])
        commodity_image_link = ','.join(images_list)
        return commodity_image_link

    def parse_name(self, div):
        a_list = div.xpath('.//h2/a[@class="a-link-normal a-text-normal"]')
        if a_list:
            a_elem = a_list[0]
            commodity_link = a_elem.attrib.get('href')
            commodity_link = SOURCE_URL + commodity_link
            describe = a_elem.xpath('./span/text()')
            if describe:
                commodity_describe = describe.get()
            else:
                commodity_describe = ''
        else:
            return None, None, None
        if ':' in commodity_describe:
            commodity_name, commodity_describe = commodity_describe.split(':', 1)
        else:
            commodity_name = commodity_describe
            commodity_describe = ''
        return commodity_name, commodity_describe, commodity_link

    def parse_star(self, div):
        span = div.xpath('.//span[@class="a-icon-alt"]/text()')
        if span:
            commodity_star = float(span[0].get().split(' ')[0])
        else:
            commodity_star = 1
        return commodity_star

    def parse_review_count(self, div):
        span = div.xpath('.//a/span[@class="a-size-base"]/text()')
        print(span)
        if span:
            commodity_review_count = span[0].get().replace(',', '')
        else:
            commodity_review_count = 0
        return commodity_review_count

    def parse_price_unit(self, div):
        span = div.xpath('.//span[@class="a-price-symbol"]/text()')
        if span:
            price_unit = span[0].get()
        else:
            price_unit = None
        return price_unit

    def parse_price(self, div):
        span = div.xpath('.//span[@class="a-price-whole"]/text()')
        if span:
            commodity_favorable_price = span[0].get().replace(',', '')
        else:
            commodity_favorable_price = None
        span = div.xpath('.//span[@class="a-price a-text-price"]/span[@class="a-offscreen"]/text()')
        if span:
            commodity_current_price = span[0].get().replace(',', '')
        else:
            commodity_current_price = commodity_favorable_price
        return commodity_favorable_price, commodity_current_price

    def parse_book(self, response, **kwargs):
        div_lists = response.xpath('//div[@data-asin]')
        results = []
        commodity_type = kwargs.get('category')
        for div in div_lists:
            _ = []
            commodity_amazonid = div.attrib.get('data-asin')
            if not commodity_amazonid:
                continue
            commodity_image_link = self.parse_images(div)
            commodity_name, commodity_describe, commodity_link = self.parse_name(div)
            if not commodity_name or not commodity_link:
                continue
            commodity_star = self.parse_star(div)
            commodity_review_count = self.parse_review_count(div)
            price_unit = self.parse_price_unit(div)
            if not price_unit:
                continue
            commodity_favorable_price, commodity_current_price = self.parse_price(div)
            if not commodity_favorable_price or not commodity_current_price:
                continue
            commodity_current_price = commodity_current_price.strip(price_unit)
            _ = [
                commodity_amazonid, commodity_image_link, commodity_name, commodity_describe,
                commodity_star, int(commodity_review_count), price_unit, float(commodity_favorable_price),
                float(commodity_current_price), commodity_link, commodity_type
            ]
            results.append(_)
            self.insert_data(results)



    def insert_data(self, results):
        cursor = self.conn.cursor()
        sql = """
            insert into commodity.commodity_list(commodity_amazonid, commodity_image_link, commodity_name,
            commodity_describe, commodity_star, commodity_review_count, price_unit, commodity_favorable_price,
            commodity_current_price, commodity_link, commodity_type) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(sql, results)
        self.conn.commit()
        cursor.close()
