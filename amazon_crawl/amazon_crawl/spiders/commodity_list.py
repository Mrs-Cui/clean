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
    name = 'commoidty_list'

    def start_requests(self):
        urls = [
            'https://www.amazon.in/'
        ]
        for url in urls:
            yield Request(url=url, callback=self.parse_class, cb_kwargs={'page': 2})

    def parse_class(self, response, **kwargs):
        options = response.xpath('//select[@id="searchDropdownBox"]/option')
        base_url = 'https://www.amazon.in/s?ref=nb_sb_noss_1&{params}'
        for option in options:
            content = option.xpath('./text()').get()
            value = option.attrib.get('value')
            if not value:
                continue
            for i in range(kwargs.get('page', 1)):
                url = base_url.format(params=parse.urlencode({'url': value, 'k': content, 'page': i}))
                yield Request(url=url, callback=self.parse_list, cb_kwargs={'category': content}, headers=HEADERS)
            break
            # yield Request(url=url, callback=self.parse_list, cb_kwargs={'category': content}, headers=HEADERS)
            # if 'book' in url:
            #     yield Request(url=url, callback=self.parse_book_home_page, cb_kwargs={'category': content}, headers=HEADERS)
            # elif 'watch' in url:
            #     yield Request(url=url, callback=self.parse_watch_home_page, cb_kwargs={'category': content}, headers=HEADERS)
            # elif 'videogame' in url:
            #     yield Request(url=url, callback=self.parse_videogame_home_page, cb_kwargs={'category': content}, headers=HEADERS)
            # elif 'sporting' in url:
            #     yield Request(url=url, callback=self.parse_sporting_home_page, cb_kwargs={'category': content}, headers=HEADERS)
            # else:
            #     yield Request(url=url, callback=self.parse_home_page, cb_kwargs={'category': content}, headers=HEADERS)

    def parse_home_page(self, response, **kwargs):
        pass

    def parse_book_home_page(self, response, **kwargs):
        urls = [
            'https://www.amazon.in/s?i=stripbooks&bbn=21090939031&rh=n%3A976389031%2Cn%3A1318447031%2Cn%3A1318449031%2Cn%3A21090939031%2Cn%3A21090942031%2Cp_85%3A10440599031%2Cp_6%3AAT95IG9ONZD7S%2Cp_n_availability%3A1318484031&pf_rd_i=21090939031&pf_rd_m=A1K21FY43GMZF8&pf_rd_p=da394964-6ed4-439a-85e3-54e5ef7e404f&pf_rd_r=26Q56TT5B85ZT9GY9E7N&pf_rd_s=merchandised-search-4&pf_rd_t=101&ref=s9_acsd_hps_bw_c2_x_c2cl',
            'https://www.amazon.in/s?i=stripbooks&bbn=21090939031&rh=n%3A976389031%2Cn%3A1318447031%2Cn%3A1318449031%2Cn%3A21090939031%2Cn%3A21090947031%2Cp_85%3A10440599031%2Cp_6%3AAT95IG9ONZD7S%2Cp_n_availability%3A1318484031&pf_rd_i=21090939031&pf_rd_m=A1K21FY43GMZF8&pf_rd_p=93cdb95f-661e-40b3-80de-55036812dd32&pf_rd_r=26Q56TT5B85ZT9GY9E7N&pf_rd_s=merchandised-search-6&pf_rd_t=101&rw_html_to_wsrp=1&ref=s9_acsd_hps_bw_c2_x_c2cl'
            'https://www.amazon.in/s?i=stripbooks&bbn=21090939031&rh=n%3A976389031%2Cn%3A1318447031%2Cn%3A1318449031%2Cn%3A21090939031%2Cn%3A21090948031%2Cp_85%3A10440599031%2Cp_6%3AAT95IG9ONZD7S%2Cp_n_availability%3A1318484031&pf_rd_i=21090939031&pf_rd_m=A1K21FY43GMZF8&pf_rd_p=7f05c27a-59ac-4a39-84be-8e26f764ff13&pf_rd_r=26Q56TT5B85ZT9GY9E7N&pf_rd_s=merchandised-search-9&pf_rd_t=101&ref=s9_acsd_hps_bw_c2_x_c2cl'
        ]
        for url in urls:
            yield response.follow(url, callback=self.parse_book_home_page, cb_kwargs=kwargs, headers=HEADERS)

    def parse_watch_home_page(self, response, **kwargs):
        pass

    def parse_videogame_home_page(self, response, **kwargs):
        pass

    def parse_sporting_home_page(self, response, **kwargs):
        pass

    def parse_list(self, response, **kwargs):
        div_lists = response.xpath('//div[@data-asin]')
        results = []
        commodity_type = kwargs.get('category')
        for div in div_lists:
            _ = []
            commodity_amazonid = div.attrib.get('data-asin')
            if not commodity_amazonid:
                continue
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
            print(div.xpath('.//h5'))
            print(div.xpath('.//h5[@class="s-line-clamp-1"]/span'))
            names = div.xpath('.//h5/span[@dir="auto"]/text()')
            print(names)
            if names:
                commodity_name = names[0].get()
            else:
                continue
            print(commodity_name)
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
                continue
            print(commodity_link)
            print(commodity_describe)
            span = div.xpath('.//span[@class="a-icon-alt"]/text()')
            if span:
                commodity_star = float(span[0].get().split('')[0])
            else:
                continue
            print(commodity_star)
            span = div.xpath('.//span[@class="a-size-base"]/text()')
            if span:
                commodity_review_count = span[0].get()
            else:
                commodity_review_count = 0
            span = div.xpath('.//span[@class="a-price-symbol"]/text()')
            if span:
                price_unit = span[0].get()
            else:
                continue
            print(price_unit)
            span = div.xpath('.//span[@class="a-price-whole"]/text()')
            if span:
                commodity_favorable_price = span[0].get()
            else:
                continue
            print(commodity_favorable_price)
            span = div.xpath('.//span[@class="a-offscreen"]/text()')
            if span:
                commodity_current_price = float(span[0].get().strip(price_unit).replace(',', ''))
            else:
                continue
            print(commodity_current_price)
            _ = [
                commodity_amazonid, commodity_image_link, commodity_name, commodity_describe,
                commodity_star, commodity_review_count, price_unit, commodity_favorable_price,
                commodity_current_price, commodity_link, commodity_type
            ]
            results.append(_)
        print(results)



