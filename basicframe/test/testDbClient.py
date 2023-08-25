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


    k = DbClient("mongodb://root:root123456@106.15.10.74:27017/admin")

    k.change_table('siteinfo')
    my_pipeline = [
        {'$match': {'type': '00'}},
        {'$sample': {'size': 5}}
    ]

    result_custom = k.get(pipeline=my_pipeline)
    print(len(result_custom))
    print(result_custom)
if __name__ == '__main__':
    testDbClient()
