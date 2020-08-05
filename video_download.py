#! /usr/bin/env python
#-*-coding:utf-8-*-

import traceback
import re
import hashlib
import os
import sys
from requests import get, post, head

VIDEO_URL_PATTERN = re.compile('.*.ts')

class VideoDownload(object):

    METHOD = {
        'GET': get,
        'POST': post,
        'HEAD': head,
    }

    HEADERS = {
        'Origin': 'https://www.caoni1.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'
    }

    def __init__(self, init_url):
        self.init_url = init_url

    def handel_request(self, url, method='GET', params=None):
        if not params:
            params = {}
        try:
            times = 0
            content = ''
            response = self.METHOD[method](url, **params)
            if response.status_code == 200:
                content = response.content
                print('request success url: [{0}]'.format(url))
            else:
                while times <= 3:
                    response = self.METHOD[method](url, **params)
                    if response.status_code == 200:
                        content = response.content
                    else:
                        times += 1
            if times > 3:
                print('request failed url: [{0}]'.format(url))
        except Exception as e:
            print('request failed url: [{0}], error: [{1}]'.format(url, traceback.format_exc()))
            content = ''
        return content

    def handle_init_url(self):
        params = {
            'headers': self.HEADERS,
            'cert': '/other/wwwcaoni1com.crt',
            'verify': True
        }
        content = self.handel_request(self.init_url, params=params)
        content = str(content, encoding='utf-8')
        base_url = '/'.join(self.init_url.split('/')[:-1])
        videos_list = content.split('\n')
        video_urls = []
        for video_str in videos_list:
            url = VIDEO_URL_PATTERN.search(video_str)
            if url:
                url = '/'.join([base_url, url.group()])
                video_urls.append(url)
        return video_urls

    def handel_video(self, urls):
        params = {
            'headers': self.HEADERS,
            'cert': '/other/wwwcaoni1com.crt',
            'verify': True
        }
        md5 = hashlib.md5()
        md5.update(urls[0].encode('utf-8'))
        md5_str = md5.hexdigest()
        dir_path = self.create_dir(md5_str)
        for url in urls:
            file_name = url.split('/')[-1]
            file_path = os.path.join(dir_path, file_name)
            print('request start, url: [{0}]'.format(url))
            content = self.handel_request(url, params=params)
            if not content:
                break
            with open(file_path, 'bw') as file:
                file.write(content)

    def create_dir(self, md5_str):
        dir_path = os.path.join('/other', md5_str)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        return dir_path




if __name__ == '__main__':
    video = VideoDownload('https://cdn.cdn-xxx.com/videos/20200424/YiZ98UDg/500kb/hls/index.m3u8')
    video_urls = video.handle_init_url()
    video.handel_video(video_urls)
