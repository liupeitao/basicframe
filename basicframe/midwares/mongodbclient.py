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

from pymongo import MongoClient
from redis.exceptions import TimeoutError, ConnectionError, ResponseError
from redis.connection import BlockingConnectionPool

from random import choice
from redis import Redis
import json

from basicframe.midwares.dbclient import DbClient
from basicframe.settings import MONGO_DB, MONGO_COLL
from basicframe.utils.logHandler import LogHandler


class MongodbClient(DbClient):
    """
    MongoDB client

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
        self.db = MONGO_DB
        self.coll = MONGO_COLL
        kwargs.pop("db")
        self.__conn = MongoClient(**kwargs)

    def get(self):
        """
        返回一个url 爬取
        :return:
        """
        document = self.__conn[self.db][self.coll].aggregate([{'$sample': {'size': 1}}])
        print(document)
        return document

    def put(self, site_info):
        """
        将代理放入hash, 使用changeTable指定hash name
        :param site_info:  一个网站的信息， 对应需求表格的一行
        :param queue_name:  存放的队列名称
        :return:
        """
        result = self.__conn[self.db][self.coll].insert_one(site_info)
        return result

    def pop(self):
        """
        随机弹出一个网站信息
        :
        """
        document = self.__conn[self.db][self.coll].find_one_and_delete({})
        return document

    def delete(self, condition):
        """
        移除指定代理, 使用changeTable指定hash name
        :param condition:
        :param queue_name:
        :return:
        """
        result = self.__conn[self.db][self.coll].delete_one(condition)
        return result.deleted_count == 1

    def exists(self, condition):
        document = self.__conn[self.db][self.coll].find_one(condition)
        return True if document else False

    def update(self, condition):
        """
        更新 site_info 属性
        :param :
        :return:
        """
        result = self.__conn[self.db][self.coll].update_one(condition)
        return result.modified_count == 1

    def get_all(self, **kwargs):
        """
        字典形式返回所有网站信息, 使用changeTable指定hash name
        :return:
        """
        return self.get_collection_cursor(**kwargs)

    def get_collection_cursor(self, **kwargs):
        cursor = self.__conn[self.db][self.coll].find(**kwargs)
        return cursor

    def clear(self):
        """
        清空所有代理, 使用changeTable指定hash name
        :return:
        """
        result = self.__conn[self.db][self.coll].delete_many({})
        return result.deleted_count

    def get_count(self):
        """
        :return:
        """
        count = self.__conn[self.db][self.coll].estimated_document_count()
        return count

    def get_count_by_condition(self, condition=None):
        if condition is None:
            condition = {}
        count = self.__conn[self.db][self.coll].count_documents(condition)
        return count

    def change_table(self, coll):
        """
        切换操作对象
        :param queue_name:
        :return:
        """
        self.coll = coll

    def test(self):
        log = LogHandler('mongo_client')
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

    def get_all_keyword(self):
        # return super().get_all_keyword()
        raise NotImplementedError

