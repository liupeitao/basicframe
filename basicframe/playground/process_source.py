from basicframe.midwares.dbclient import DbClient
mongo_conn = DbClient('mongodb://root:root123456@106.15.10.74:27017/admin')
mongo_conn.change_table('test')
print(mongo_conn.get())
