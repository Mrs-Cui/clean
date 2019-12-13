#! /usr/bin/env python
# -*- coding:utf-8 -*-
from psycopg2.pool import ThreadedConnectionPool

from concurrent.futures import ThreadPoolExecutor

import random
import time



APP_DATABASE = {
    # 'com.live.videochat': 'app300032',
    # 'com.vc.perform.mmshow.pro': 'app300038',
    # 'com.vc.perform.mmshow.turkey': 'app300039',
    # 'com.random.live.video.chat.global': 'app300040',
    # 'com.moca.chat': 'app300041',
    # 'com.jily.chat': 'app300042',
    # 'com.cooma.chat': 'app300043',
    # 'com.hiyaa.videochat': 'app300045',
    # 'com.videochat.live.vaka': 'app300046',
    # 'com.lovemumu.videochat': 'app300047',
    'com.jily.find.with': {'bi': 'app300052', 'app_name': 'Jily', 'redshiftId': 4},
    # 'com.social.videosns': {'bi': 'app300048', 'app_name': 'Veego（iOS）', 'redshiftId': 4},
    'com.live.videochat.india': {'bi': 'app300049', 'app_name': 'ZAKZAK Pro', 'redshiftId': 4},
    'com.wegochat.happy': {'bi': 'app300053', 'app_name': 'Veego(Android)', 'redshiftId': 4},
    'com.live.veegopro.chat': {'bi': 'app300056', 'app_name': 'Yepop(Android)', 'redshiftId': 4},
    'com.live.zakzak.chat': {'bi': 'app300055', 'app_name': 'ZAKZAK Live(Android)', 'redshiftId': 4},
    'com.zakzak.chat': {'bi': 'app300051', 'app_name': 'ZAKZAK Live(iOS)', 'redshiftId': 4},
    'com.topu.livechat': {'bi': 'app300058', 'app_name': 'TopU', 'redshiftId': 4},
    'com.parau.videochat': {'bi': 'app300061', 'app_name': 'ParaU/Yepop(iOS)', 'redshiftId': 3},
    'com.hoogo.hoogo': {'bi': 'app300063', 'app_name': 'Hoogo/Valla', 'redshiftId': 3},
    'com.mecoo.chat': {'bi': 'app300065', 'app_name': 'Mecoo', 'redshiftId': 3},
    'com.mumu.videochat': {'bi': 'app300066', 'app_name': 'MuMu', 'redshiftId': 3},
    'com.mumu.videochat.india': {'bi': 'app300070', 'app_name': 'MuMu India', 'redshiftId': 3},
    'com.parau.pro.videochat': {'bi': 'app300072', 'app_name': 'ParaU Pro', 'redshiftId': 3},
    'com.mecoolive.chat': {'bi': 'app300069', 'app_name': 'Mecoo Live', 'redshiftId': 3},
    'com.fachat.freechat': {'bi': 'app300076', 'app_name': 'Fachat', 'redshiftId': 3}
    # 'com.friends.chat.valla': {'bi': 'app300063', 'app_name': 'Valla'},
    # 'com.zakzak.chat.web': 'app300054',
}
event = [{'bi': v['bi'], 'redshiftId': v['redshiftId']} for k, v in APP_DATABASE.items()]
REDSHIFT3_CONNECTION_INFO = {
    'dsn': 'dbname=dev user=lbeconsumer1 password=gCkevYfKo4Xz '
           'host=lbe-events-3.c2t6uywzhjvz.us-west-2.redshift.amazonaws.com port=5439',  # NOQA
    'min': 20,
    'max': 500,
    'param': {
        'host': 'lbe-events-3.c2t6uywzhjvz.us-west-2.redshift.amazonaws.com',
        'port': 5439,
        'user': 'lbeconsumer1',
        'password': 'gCkevYfKo4Xz',
        'database': 'dev',
    },
    'async': 1
}

REDSHIFT4_CONNECTION_INFO = {
    'dsn': 'dbname=dev user=lbeconsumer1 password=gCkevYfKo4Xz '
           'host=lbe-events-4.c2t6uywzhjvz.us-west-2.redshift.amazonaws.com port=5439',  # NOQA
    'min': 20,
    'max': 500,
    'param': {
        'host': 'lbe-events-4.c2t6uywzhjvz.us-west-2.redshift.amazonaws.com',
        'port': 5439,
        'user': 'lbeconsumer1',
        'password': 'gCkevYfKo4Xz',
        'database': 'dev',
    },
    'async': 1
}
redshift3_conn_poll = ThreadedConnectionPool(REDSHIFT3_CONNECTION_INFO['min'], REDSHIFT3_CONNECTION_INFO['max'],
                                            **REDSHIFT3_CONNECTION_INFO['param'])
redshift4_conn_poll = ThreadedConnectionPool(REDSHIFT4_CONNECTION_INFO['min'], REDSHIFT4_CONNECTION_INFO['max'],
                                            **REDSHIFT4_CONNECTION_INFO['param'])
connPoolMap = {
    3: redshift3_conn_poll,
    4: redshift4_conn_poll
}
def gevent_test():
    task_pool = ThreadPoolExecutor(20)
    results = []
    jid = 'user_7761444@vshow-euc1.1-1.io'
    data_list = []
    start = time.time()

    for table_obj in event:
        table = table_obj['bi']
        redshiftId = table_obj['redshiftId']
        table = table + '.events'
        conn_pool = connPoolMap[redshiftId]
        conn = conn_pool.getconn()
        # log_info.info('table: [{0}], redishift_id: [{1}]'.format(table, redshiftId))
        results.append(task_pool.submit(async_query_jid, table, redshiftId, conn, u_jid=jid, user_id=None))
    task_pool.shutdown()
    for result in results:
        data_list.extend(result.result())
    end = time.time()
    print('spend time: %s' % (end - start))
def async_query_jid(table, redishift_id, conn, user_id=None, u_jid=None):
    sql = "select distinct user_id, u_jid from {0}".format(table)
    query = []
    params = []
    data_list = []
    if user_id:
        query.append('user_id in %s and u_jid is not null')
        params.append(tuple(user_id))
    if u_jid:
        query.append('u_jid = %s and user_id is not null')
        params.append(u_jid)
    if query:
        sql = ' '.join([sql, 'where', ' and '.join(query)])
    print('查询开始: table: [{0}], redishiftid: [{1}]'.format(table, redishift_id))
    # time.sleep(random.randint(1,5))
    rows = query_result(sql, redishift_id, conn=conn, params=params)
    # data_list.extend([{'user_id': r[0], 'jid': r[1]} for r in rows if r[0]])
    print('查询结束: table: [{0}], redishiftId: [{1}], results: [{2}], sql: [{3}], params: [{4}]'.format(table, redishift_id, data_list, sql, params))
    return data_list


def release_redshift_connection(conn, redshiftId):
    if conn:
        _coolPool = connPoolMap[redshiftId]
        _coolPool.putconn(conn)


def query_result(sql, redshiftId=4, params=None, conn=None):
    #
    if not sql:
        return

    # conn = get_redshift_connection(redshiftId)
    try:
        #
        cursor = conn.cursor()
        #
        if not params:
            cursor.execute(sql)
        else:
            cursor.execute(sql, params)
        #
        items = cursor.fetchall()
        #
        cursor.close()
    except Exception as e:
        raise e
    finally:
        release_redshift_connection(conn, redshiftId)
    return items

if __name__ == '__main__':
    gevent_test()
