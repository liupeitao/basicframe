from pymongo import MongoClient

# MongoDB 连接信息
db_name = 'mulwenben'
mongo_url = 'mongodb://root:root123456@106.15.10.74:27017/admin'
coll_name = 'siteinfo'

client = MongoClient(mongo_url)
db = client[db_name]
collection = db[coll_name]

# 找出所有重复的 start_url
pipeline = [
    {
        '$group': {
            '_id': '$start_url',
            'uniqueIds': {
                '$addToSet': '$_id'
            },
            'count': {
                '$sum': 1
            }
        }
    },
    {
        '$match': {
            'count': {
                '$gt': 1
            }
        }
    }
]

duplicates = list(collection.aggregate(pipeline))

for duplicate in duplicates:
    # 保留第一个文档，删除其余文档
    ids_to_remove = duplicate['uniqueIds'][1:]
    for id in ids_to_remove:
        collection.delete_one({'_id': id})

print("Finished removing duplicates.")
