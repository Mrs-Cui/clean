#! /usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import random
import hashlib
import json
import execjs
import os
import sys

APP_ID = "20190902000331247"
SECRET_KEY = "oYj71tzHmLQwLbogKKHk"
API_URL = "http://api.fanyi.baidu.com/api/trans/vip/translate?"

base_path = os.path.dirname(os.path.abspath(__file__))

[
    'com.vc.perform.mmshow.turkey', 'com.video.hilachat',
    'com.live.videochat.india', 'com.moca.videochat',
    'com.cooma.chat', 'com.vika.vikachat', 'com.game.cutemeet',
    'com.videochat.live.vaka', 'com.randomchat.live', 'com.friends.chat.valla',
    'com.moca.chat', 'com.social.videosns', 'com.match.u.chat', 'com.vc.perform.mmshow.pro',
    'com.live.videochat', 'com.blabla.videochat', 'com.hiyaa.videochat',
    'com.wegochat.happy', 'com.random.live.video.chat.global']

EMAIL_ADDRESS = {
    ('com.parau.pro.videochat', 'com.parau.videochat', 'com.parau.chat'): 'paraucsteam@gmail.com',
    ('com.lovemumu.videochat', 'com.mumu.videochat', 'com.mumu.videochat.india'): 'mumucsteam@gmail.com',
    ('com.Yepop.chat', 'com.yepop.videochat',): 'yepopcsteam@gmail.com',
    ('com.mecoo.chat', 'com.mecoolive.chat',): 'tinnercsteam@gmail.com',
    ('com.live.veegopro.chat',): '	veegocsteam@gmail.com',
    ('com.jily.find.with', 'com.jily.chat',): 'Jilyteam@gmail.com',
    ('com.topu.livechat',): 'topucsteam@gmail.com',
    ('com.hoogo.hoogo',): 'zakzakliveteam@gmail.com',

}


# 百度API 翻译

def lang_translate(content, source, target):
    random_value = random.randint(32768, 65536)
    sign = ''.join([APP_ID, content, str(random_value), SECRET_KEY])
    md5 = hashlib.md5()
    md5.update(sign.encode('utf-8'))
    sign = md5.hexdigest()
    params = {
        'q': content,
        'appid': APP_ID,
        'from': source,
        'to': target,
        'salt': str(random_value),
        'sign': sign
    }
    proxies = {'http': 'socks5://192.168.2.244:9091', 'https': 'socks5://192.168.2.244:9091'}
    response = requests.get(API_URL, params=params, proxies=proxies)
    print(response.text)
    result = json.loads(response.text)
    print(type(result))
    print(len(result['trans_result']))
    print(result['trans_result'][0]['dst'])


# google 翻译

def google_translate(content, source, target):
    google_api = "https://translate.google.cn/translate_a/single?client=webapp&sl={sl}&tl={tl}&hl={hl}&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&q={q}"
    headers = {
        'user-agent': 'ozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'authority': 'translate.google.cn'
    }
    url = google_api.format(sl=source, tl=target, hl=target, q=content)
    tk = execl_js(content)
    url += tk
    proxies = {'http': 'socks5://192.168.2.244:9091', 'https': 'socks5://192.168.2.244:9091'}
    response = requests.get(url, headers=headers, proxies=proxies)
    print(response.text)


def execl_js(content):
    file_path = os.path.join(base_path, 'google_tk_parame.js')
    with open(file_path, 'r+') as file:
        js_str = file.read()
    phantomjs = execjs.get('PhantomJS')
    js_compile = phantomjs.compile(js_str)
    tk = js_compile.call('get_tk_parame', content)
    print(tk)
    return tk

import requests
def request_func():
    url = "https://api.payoneer.com/v2/programs/100121170/payees/123456/status"
    response = requests.get(url, auth=('Yepop1170', 'meetstar123'))
    print(response.text)
if __name__ == '__main__':
    # string = "Your account has been frozen for 4 hours for inappropriate contents. Your account will be unblocked after the countdown ends."
    # string = "Your account has been blocked for inappropriate behaviors."
    # string = "If you have any questions, please contact us at paraucsteam@gmail.com"
    # string = "The views have optional arguments you can use to alter the behavior of the view. For example, if you want to change the template name a view uses, you can provide the template_name argument. A way to do this is to provide keyword arguments in the URLconf, these will be passed on to the view. For example:"
    # google_translate(string, 'en', 'zh-CN')
    request_func()
