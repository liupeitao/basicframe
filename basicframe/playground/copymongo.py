import pymongo

# MongoDB 的连接信息
MONGO_URL = "mongodb://root:root123456@106.15.10.74:27017/admin"

# 连接到 MongoDB
client = pymongo.MongoClient(MONGO_URL)

# 获取原始集合
source_db = client["mulwenben"]
source_collection = source_db["siteinfo"]

# 获取目标数据库和集合
target_db = client["test"]
target_collection = target_db["siteinfo"]

# 复制数据
documents = list(source_collection.find({}))
target_collection.insert_many(documents)

print(f"Copied {len(documents)} documents from 'mulwenben.siteinfo' to 'test.siteinfo'.")

# 关闭 MongoDB 连接
client.close()
