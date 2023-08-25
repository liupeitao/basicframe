import re

import pymongo
import json




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
db = client["article"]  # 替换为你要导出的数据库名字

process_one_coll(db['https://www.sportskeeda.com/go/serie-a-calcio/news_2023_08_16'], 'sportskeeda')

print("所有集合导出完成")