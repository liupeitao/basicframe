# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     testDbClient
   Description :
   Author :        JHao
   date：          2020/6/23
-------------------------------------------------
   Change Activity:
                   2020/6/23:
-------------------------------------------------
"""
__author__ = 'JHao'

from basicframe.midwares.dbclient import DbClient


def testDbClient():
    #  ############### ssdb ###############
    # ssdb_uri = "ssdb://:password@127.0.0.1:8888"
    # s = DbClient.parse_db_conn(ssdb_uri)
    # assert s.db_type == "SSDB"
    # assert s.db_pwd == "password"
    # assert s.db_host == "127.0.0.1"
    # assert s.db_port == 8888


    k = DbClient("redis://:qunyin@123@101.35.228.6:6379/2")
    assert k.db_type == "REDIS"
    assert k.db_pwd == "qunyin@123"
    assert k.db_host == "101.35.228.6"
    assert k.db_port == 6379
    assert k.db_name == "2"
    k.change_table('网站信息')
    print(k.get_all())

if __name__ == '__main__':
    testDbClient()
