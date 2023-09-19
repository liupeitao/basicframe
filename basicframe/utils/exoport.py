import re

import pymongo
import json

# client = pymongo.MongoClient("mongodb://admin:Liupeitao1.@localhost:27017/admin")
# db = client["articel"]
# collection = db['ouguan']
#
# data = collection.find({}, {'_id': 0})
#
# now = open('ougu1an.json', mode='r').read()
#
# pattern = re.compile('"url": "(http.*)", "domain"')
# all_url = set(pattern.findall(now))
# with open("ouguan01801.json", "w") as file:
#     for document in data:
#         if not document['url'] in all_url:
#             print(document)
#             # json.dump(document, file)
#             file.write(json.dumps(document))
#             file.write('\n')
#
# print("数据已成功导出到 data.json 文件中")
import re


def process_one_coll(collection, file_name):
    data = collection.find({}, {'_id': 0})
    with open(f"../assets/{file_name}.json", "w") as file:
        for document in data:
            # if not document['url'] in all_url:
            print(document)
            file.write(json.dumps(document, ensure_ascii=False))
            file.write('\n')

    print("数据已成功导出到 data.json 文件中")


from basicframe.midwares.mongodbclient import MongoDBClient
client = MongoDBClient().connect()
db = client["defalult_db"]  # 替换为你要导出的数据库名字
# collection_names = db.list_collection_names()

process_one_coll(db['https://www.thedrive.com/the-war-zone'])
#
# for name in collection_names:
#     process_one_coll(db[name], name)

# for collection_name in collection_names:
#     collection = db[collection_name]
#     documents = collection.find()
#     file_name = f"assets/{collection_name}.json"
#
#     with open(file_name, "w") as file:
#         for document in documents:
#             item = json.dumps(document)
#             file.write(item)
#             file.write('\n')

    # print(f"集合 {collection_name} 已成功导出到文件 {file_name}")

print("所有集合导出完成")