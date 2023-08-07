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
        # 将数据插入到MongoDB中
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

if __name__ == '__main__':
    domain_info = {
        "url": 'https://www.thedrive.com/the-war-zone',
        'domains': '政治',
        'selector': {
            'type': 'Partial | Static',
            'item_xpath_restrict': '//main',
            'page_xpath_restrict': '//pagination'
        }
    }
    domain = 'https://www.thedrive.com/the-war-zone'
    mongo_client = MongoDBClient()
    mongo_client.save_site_info_to_mongodb(domain,  'test', 'site_info_test', **domain_info)