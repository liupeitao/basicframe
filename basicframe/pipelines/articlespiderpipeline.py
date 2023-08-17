import scrapy
from datetime import datetime

from scrapy.utils.project import get_project_settings

from basicframe.midwares.mongodbclient import MongoDBClient

mongo_client = MongoDBClient().connect()


class ArticleSpiderPipeline:
    settings = get_project_settings()

    def open_spider(self, spider: scrapy.Spider):
        self.db = mongo_client[spider.settings['MONGO_DB']]
        coll_name = self.generate_name(spider.name)
        self.collection = self.db[coll_name]

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        if len(item['content']) > 100:
            item = dict(item)
            print(item)
            self.collection.insert_one(item)

    def generate_name(self, str):
        now = datetime.now()
        time_str = now.strftime("%Y_%m_%d")
        return f"{str}_{time_str}"
