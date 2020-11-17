#! /usr/bin/env python
from gevent.pool import Pool
import requests
import time

import threading
from threading import Thread

def main():
    task_pool = Pool(200)
    threads = []
    for i in range(2000):
        thread = Thread(target=handle, args=(i,))
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def handle(index):
    response = requests.get('http://127.0.0.1:6667/handle')
    print(index, response.status_code, response.content)

if __name__ == '__main__':
    start = time.time()
    main()
    print(time.time() - start)