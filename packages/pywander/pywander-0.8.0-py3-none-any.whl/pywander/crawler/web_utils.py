#!/usr/bin/env python
# -*-coding:utf-8-*-

import logging
import requests
import threading
from datetime import timezone
from dateutil.relativedelta import relativedelta

from my_fake_useragent import UserAgent

from .cache_utils import func_cache, cachedb
from pywander.datetime import timestamp_current, timestamp_to_dt, dt_current

logger = logging.getLogger(__name__)

ua = UserAgent(family=['chrome', 'firefox'])


def _update_requests_web(cache_data, args):
    logger.info('update_requests_web')
    headers = {
        'user-agent': ua.random()
    }
    url = args[0]
    data = requests.get(url, headers=headers, timeout=30)

    cache_data['data'] = data
    cache_data['timestamp'] = str(timestamp_current())
    key = cache_data.get('key')

    cachedb.set(key, cache_data)
    return data


def use_cache_callback_requests_web(cache_data, func, args, kwargs,
                                    use_cache_oldest_dt=None):
    timestamp = cache_data.get('timestamp', timestamp_current())
    data_dt = timestamp_to_dt(timestamp)

    if use_cache_oldest_dt is None:
        target_dt = dt_current() - relativedelta(seconds=14)  # default 14 days
    else:
        target_dt = use_cache_oldest_dt


    if data_dt.tzinfo is None:
        data_dt.replace(tzinfo=timezone.utc)
    if target_dt.tzinfo is None:
        target_dt.replace(tzinfo=timezone.utc)

    if data_dt < target_dt:  # too old then we will re-excute the function
        t = threading.Thread(target=_update_requests_web,
                             args=(cache_data, args))
        t.daemon = True
        t.start()


@func_cache(use_cache_callback=use_cache_callback_requests_web)
def requests_web(url):
    """
    有数据则缓存中直接使用 没有数据则试着从网络上请求
    直接使用数据的时候会根据数据的时间戳来判断新旧，如果数据过旧则启动后台更新线程

    :param url:
    :return:
    """
    headers = {
        'user-agent': ua.random()
    }

    data = requests.get(url, headers=headers, timeout=30)

    return data
