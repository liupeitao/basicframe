# from pymongo import MongoClient
# import basicframe.settings as settings
#
# class MongoDBClient:
#     _instance = None
#     mongo_url = settings.MONGO_URL
#
#     def connect(self):
#         return MongoClient(self.mongo_url)
#
# mongo_client = MongoDBClient().connect()
import pandas as pd
from pymongo import MongoClient
import json

class MongoDBClient:
    def __init__(self):
        self.client = None
    def connect(self):
        if self.client is None:
            self.client = MongoClient('mongodb://root:root123456@106.15.10.74:27017/admin')
        return self.client


    def save_site_info_to_mongodb(self, domain, db_name, coll,  **kwargs):
        # 连接到MongoDB
        collection = MongoDBClient().connect()[db_name][coll]
        collection.insert_one({str(domain): json.dumps(kwargs, ensure_ascii=False)})


    def get_site_info_from_mongodb(self, domain, db_name, coll) -> dict:
        # 连接到MongoDB
        collection = MongoDBClient().connect()[db_name][coll]
        # 获取指定域名的文档
        doc = collection.find_one({str(domain): {"$exists": True}})
        if doc:
            domain_info_dict = json.loads(doc[str(domain)])
            return domain_info_dict
        else:
            return {}

    from pymongo import MongoClient

    def update_siteinfo_status(self, database_name, collection_name, new_status):
        # 连接到 MongoDB
        collection = MongoDBClient().connect()[database_name][collection_name]
        # 更新所有文档的 siteinfo 字段，添加一个 status 字段
        collection.update_many({}, {"$set": {"status": new_status}})

    def get_address_values(self, database_name, collection_name, field_name):
        # 连接到 MongoDB
        client = MongoDBClient().connect()
        db = client[database_name]
        collection = db[collection_name]

        # 查询所有文档并提取指定字段的值
        field_values = []
        for document in collection.find():
            field_value = document.get(field_name)
            if field_value:
                field_values.append(field_value)

        # 关闭 MongoDB 连接
        client.close()

        return field_values

def add_site_to_redis():

    # 读取 xlsx 文件
    xlsx = pd.ExcelFile('/home/liupeitao/yingwenwenben20230816.xlsx')

    # 读取每个工作表中的数据并转换为字典列表
    data = []
    she = xlsx.sheet_names[2:3]
    sheet_data = []
    for sheet_name in she:
        df = pd.read_excel(xlsx, sheet_name)
        sheet_data = df.to_dict(orient='records')

    mongo_client.connect()['articel']['siteinfo'].insert_many(sheet_data[40:])





if __name__ == '__main__':
    # domain_info = {
    #     "url": 'https://www.thedrive.com/the-war-zone',
    #     'domains': '政治',
    #     'selector': {
    #         'type': 'Partial | Static',
    #         'item_xpath_restrict': '//main',
    #         'page_xpath_restrict': '//pagination'
    #     }
    # }

    mongo_client = MongoDBClient()
    # 调用封装的函数来更新数据
    # mongo_client.update_siteinfo_status('articel','siteinfo',0)
    url_list = mongo_client.get_address_values('articel','siteinfo','地址')
    for url in url_list:
        print(url)