import redis
from pymongo import MongoClient
from basicframe.settings import MONGO_DB_MUL, MONGO_URL, MONGO_COLL_SITEINFO
from basicframe.filters.filter import judge_type

# MongoDB 连接信息
db_name = MONGO_DB_MUL
mongo_url = MONGO_URL
coll_name = MONGO_COLL_SITEINFO


class DocumentProcessor:
    def __init__(self, mongo_url, db_name, coll_name):
        self.client = MongoClient(mongo_url)
        self.db = self.client[db_name]
        self.collection = self.db[coll_name]
        self.started = False
        self.docs = None

    def fetch_one_unprocessed(self):
        """从数据库中获取一个 preprocess 为 false 的文档"""
        if not self.started:
            self.docs = self.collection.find({"preprocess": False})
            self.started = True
        yield self.docs.next()

    def fetch_one(self, pipeline):
        doc = self.collection.find_one(pipeline)
        return doc

    def fetch_random_one(self, condition):
        pipeline = [
            {"$match": condition},
            {"$sample": {"size": 1}}
        ]
        doc = self.collection.aggregate(pipeline=pipeline).next()
        return doc

    def fetch(self, pipeline):
        docs_cursor = self.collection.find(pipeline)
        return docs_cursor

    def update_as_processed(self, start_url, new_document):
        """标记文档为已处理，并替换整个文档"""
        self.collection.replace_one({"start_url": start_url}, new_document)


    def process_document(self, hook_func):
        """处理文档"""
        doc = self.fetch_random_one(condition={'vpn_need': 'unknown', 'type': '00'})
        if doc:
            processed_doc = hook_func(doc)
            logger.info(f'processed {processed_doc}')
            self.update_as_processed(doc["start_url"], processed_doc)
        else:
            print("No unprocessed document found.")

    def update(self, doc):
        self.update_as_processed(doc['start_url'], doc)


# 定义一个钩子函数
def custom_processing_hook(document):
    res = judge_type(document['start_url'])
    logger.info(f'judge_type: {res}, process {document}')
    document['preprocess'] = True
    if not res:
        document['type'] = 'unknown'
        document['status'] = 'peding'
        return document
    if res == 'full_type':
        document['type'] = '10'
    elif res == 'psp_type':
        document['type'] = '00'
    document['status'] = 'ready'
    return document


import requests

def custom_processing_vpn_need(document):
    try:
        url = document['start_url']
    except Exception as e:
        document['start_url'] = 'x'
        return document
    try:
        response = requests.get(url, timeout=10)
    except Exception as e:
        document['vpn_need'] = True
        return document

    vpn_need = response.status_code != 200
    if vpn_need:
        document['vpn_need'] = True
    else:
        document['vpn_need'] = False
    logger.info(f'{url}: vpn_need: {vpn_need}')
    return document

from basicframe.utils.logHandler import LogHandler

logger = LogHandler('process_mongo', file=True)
processor = DocumentProcessor(mongo_url, db_name, coll_name)
if __name__ == '__main__':
    while 1:
        processor.process_document(custom_processing_vpn_need)
