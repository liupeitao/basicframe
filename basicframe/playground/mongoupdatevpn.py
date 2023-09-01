from pymongo import MongoClient

# 连接到MongoDB
client = MongoClient('mongodb://root:root123456@106.15.10.74:27017/admin')

# 选择 'test' 数据库
db = client.mulwenben

# 为 'siteinfo' 集合中的所有文档添加字段 'vpn_need'，值为 'unknown'
db.siteinfo.update_many({}, {'$set': {'vpn_need': 'unknown'}})

# 关闭连接
client.close()
