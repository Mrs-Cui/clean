#-*-coding:utf-8-*-

import pymongo
import requests
import json
from gevent.pool import Pool
from concurrent.futures import ThreadPoolExecutor
import time
import sys
import os
import csv
from datetime import datetime, timedelta
from collections import defaultdict


class Ranking(object):

    def __init__(self, host=None, port=None):
        self.client = pymongo.MongoClient(host=host, port=port)
        self.ranking_table = self.client['Task']['Ranking']
        self.data_table = self.client['Data']['Ranking']
        self.HEADERS = {
            'Origin': 'https://www.wtatennis.com',
            'Referer': 'https://www.wtatennis.com/rankings/singles',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'
        }


    def create_task(self):
        start_time = datetime(year=2001, day=1, month=1)
        current_time = datetime.now()
        while start_time <= current_time:
            tasks = []
            for page in range(70):
                task = dict()
                task['page'] = page
                task['search_time'] = start_time.strftime('%Y-%m-%d')
                task['finish'] = False
                tasks.append(task)
            self.ranking_table.insert_many(tasks)
            start_time += timedelta(days=7)


    def start_task(self):
        task_pool = ThreadPoolExecutor(max_workers=5)
        results = self.ranking_table.find({'finish': False}, no_cursor_timeout=True)
        num = 0
        tmp = []
        for result in results:
            num += 1
            print(result)
            tmp.append(task_pool.submit(self.crawl_task, result))
            if num > 5:
                print([item.result() for item in tmp])
                num = 0
                tmp = []
            # self.crawl_task(result)
        task_pool.shutdown(wait=True)
        results.close()

    def crawl_task(self, task):
        url = "https://api.wtatennis.com/tennis/players/ranked?page={page}&pageSize=20&type=rankSingles&sort=asc&name=&metric=SINGLES&at={search_time}&nationality="
        url = url.format(page=task['page'], search_time=task['search_time'])
        response = requests.get(url)
        content = str(response.content, encoding='utf-8')
        if response.status_code == 200:
            content = json.loads(content)
            if content:
                self.data_table.insert_many(content)
            self.ranking_table.update({'page': task['page'], 'search_time': task['search_time']}, {'$set': {'finish': True}})
        return '-'.join([str(task['page']), task['search_time'], 'finish'])

    def handle_data(self):
        ranks = self.data_table.find({}, no_cursor_timeout=True)
        field_names = ['Rank', 'Player', 'Region', 'Age', 'Tournaments Played', 'Points']
        data = defaultdict(list)
        for rank in ranks:
            ranked_at = rank['rankedAt']
            ranked_time = ranked_at[:10]
            file_path = os.path.join('/crawl_ranking', '{0}.csv'.format(ranked_time))
            if not os.path.exists(file_path):
                with open(file_path, 'w+') as file:
                    writer = csv.DictWriter(file, fieldnames=field_names)
                    writer.writeheader()
            age = int((datetime.strptime(ranked_time, '%Y-%m-%d') -
                   datetime.strptime(rank['player']['dateOfBirth'], '%Y-%m-%d')).days / 365)
            data[ranked_time].append({
                'Rank': rank['ranking'], 'Player': rank['player']['fullName'],
                'Region': rank['player']['countryCode'], 'Age': age,
                'Tournaments Played': rank['tournamentsPlayed'], 'Points': rank['points']
            })
            if len(data[ranked_time]) >= 3000:
                with open(file_path, 'a+') as file:
                    writer = csv.DictWriter(file, fieldnames=field_names)
                    writer.writerows(data[ranked_time])
                data[ranked_time] = []
        else:
            for key in data:
                file_path = os.path.join('/crawl_ranking', '{0}.csv'.format(key))
                with open(file_path, 'a+') as file:
                    writer = csv.DictWriter(file, fieldnames=field_names)
                    writer.writerows(data[key])


if __name__ == '__main__':
    rank = Ranking()
    rank.handle_data()