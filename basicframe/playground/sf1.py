import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from basicframe.filters.filter import judge_type
from basicframe.utils.logHandler import LogHandler

# MongoDB 连接信息
db_name = 'mulwenben'
mongo_url = 'mongodb://root:root123456@106.15.10.74:27017/admin'
coll_name = 'siteinfo'

logger = LogHandler('process_mongo', file=True)


class DocumentProcessor:
    def __init__(self, mongo_url, db_name, coll_name):
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client[db_name]
        self.collection = self.db[coll_name]

    async def fetch_one_unprocessed(self):
        """从数据库中获取一个 preprocess 为 false 的文档"""
        return await self.collection.find_one({"preprocess": False})

    async def mark_as_processed(self, start_url, new_document):
        """标记文档为已处理，并替换整个文档"""
        logger.info(f'tihuan{new_document}')
        await self.collection.replace_one({"start_url": start_url}, new_document)

    async def process_document(self, hook_func):
        """处理文档"""
        doc = await self.fetch_one_unprocessed()
        if doc:
            processed_doc = hook_func(doc)
            await self.mark_as_processed(doc["start_url"], processed_doc)
        else:
            print("No unprocessed document found.")


# 定义一个钩子函数
def custom_processing_hook(document):
    res = judge_type(document['start_url'])
    logger.info(f'process {document}, judge_type: {res}')
    document['preprocess'] = True
    if not res:
        return document
    if res == 'full_type':
        document['type'] = '10'
    elif res == 'psp_type':
        document['type'] = '00'
    document['status'] = 'ready'
    return document


if __name__ == '__main__':
    processor = DocumentProcessor(mongo_url, db_name, coll_name)

    async def main():
        for _ in range(50000):
            await processor.process_document(custom_processing_hook)

    asyncio.run(main())
