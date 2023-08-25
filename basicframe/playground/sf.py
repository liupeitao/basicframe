from pymongo import MongoClient

from basicframe.filters.filter import judge_type

# MongoDB 连接信息
db_name = 'mulwenben'
mongo_url = 'mongodb://root:root123456@106.15.10.74:27017/admin'
coll_name = 'siteinfo'


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
           self.docs = self.collection.find({"preprocess": True, "type": "00"})
           self.started = True
        yield self.docs.next()



    def mark_as_processed(self, start_url, new_document):
        """标记文档为已处理，并替换整个文档"""
        logger.info(f'tihuan{new_document}')
        self.collection.replace_one({"start_url": start_url}, new_document)

    def process_document(self, hook_func):
        """处理文档"""
        doc = next(self.fetch_one_unprocessed())
        if doc:
            processed_doc = hook_func(doc)
            logger.info(f'processed {processed_doc}')
            self.mark_as_processed(doc["start_url"], processed_doc)
        else:
            print("No unprocessed document found.")


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


from basicframe.utils.logHandler import LogHandler

logger = LogHandler('process_mongo', file=True)
processor = DocumentProcessor(mongo_url, db_name, coll_name)
if __name__ == '__main__':
    while 1:
        processor.process_document(custom_processing_hook)
