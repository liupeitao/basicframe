# -*- coding: utf-8 -*-
"""
-----------------------------------------------------
   File Name：     redisclient.py
   Description :   封装Redis相关操作
   Author :        JHao
   date：          2019/8/9
------------------------------------------------------
   Change Activity:
                   2019/08/09: 封装Redis相关操作
                   2020/06/23: 优化pop方法, 改用hscan命令
                   2021/05/26: 区别http/https代理
------------------------------------------------------
"""
__author__ = 'pting'

from redis.exceptions import TimeoutError, ConnectionError, ResponseError
from redis.connection import BlockingConnectionPool

from random import choice
from redis import Redis
import json

from basicframe.utils.logHandler import LogHandler


class RedisClient(object):
    """
    Redis client

    Redis中代理存放的结构为hash：
    key为ip:port, value为代理属性的字典;

    """

    def __init__(self, **kwargs):
        """
        init
        :param host: host
        :param port: port
        :param password: password
        :param db: db
        :return:
        """
        self.name = ""
        kwargs.pop("username")
        self.__conn = Redis(connection_pool=BlockingConnectionPool(decode_responses=True,
                                                                   timeout=5,
                                                                   socket_timeout=5,
                                                                   **kwargs))


    def get(self):
        """
        返回一个url 爬取
        :return:
        """
        keys = self.__conn.hkeys(self.name)
        key = choice(keys) if keys else None
        return self.__conn.hget(self.name, key) if key else None

    def put(self, site_info):
        """
        将代理放入hash, 使用changeTable指定hash name
        :param site_info:  一个网站的信息， 对应需求表格的一行
        :param queue_name:  存放的队列名称
        :return:
        """
        data = self.__conn.hset(self.name, site_info['start_url'], json.dumps(site_info, ensure_ascii=False))
        return data

    def pop(self):
        """
        随机弹出一个start_url
        :return: dict {proxy: value}
        """
        site_info = self.get()
        if site_info:
            self.__conn.hdel(self.name, json.loads(site_info).get("start_url", ""))
        return site_info if site_info else None

    def delete(self, start_url):
        """
        移除指定代理, 使用changeTable指定hash name
        :param queue_name:
        :param start_url:
        :return:
        """
        return self.__conn.hdel(self.name, start_url)

    def exists(self, start_url):
        """
        判断指定代理是否存在, 使用changeTable指定hash name
        :param queue_name:
        :param start_url: proxy str
        :return:
        """
        return self.__conn.hexists(self.name, start_url)

    def update(self, site_info):
        """
        更新 site_info 属性
        :param :
        :return:
        """
        return self.__conn.hset(self.name, site_info['start_url'], site_info.to_json)

    def get_all(self):
        """
        字典形式返回所有网站信息, 使用changeTable指定hash name
        :return:
        """
        # items = self.__conn.hvals(self.name)
        keys = self.__conn.keys()
        return keys

    def clear(self):
        """
        清空所有代理, 使用changeTable指定hash name
        :return:
        """
        return self.__conn.delete(self.name)

    def get_count(self):
        """
        返回代理数量
        :return:
        """
        items = self.get_all()
        return {'total': len(items)}

    def change_table(self, queue_name):
        """
        切换操作对象
        :param queue_name:
        :return:
        """
        self.name = queue_name

    def test(self):
        log = LogHandler('redis_client')
        try:
            self.get_count()
        except TimeoutError as e:
            log.error('redis connection time out: %s' % str(e), exc_info=True)
            return e
        except ConnectionError as e:
            log.error('redis connection error: %s' % str(e), exc_info=True)
            return e
        except ResponseError as e:
            log.error('redis connection error: %s' % str(e), exc_info=True)
            return e

