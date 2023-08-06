# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from scrapy.utils.project import get_project_settings

from basicframe.midwares.mongodbclient import mongo_client


class ArticleSpiderPipeline:
    settings = get_project_settings()

    def open_spider(self, spider: scrapy.Spider):
        self.db = mongo_client[spider.settings['MONGO_DB']]


    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        if len(item['content']) > 200:
            coll_name = item.get('netloc') or spider.name
            collection = self.db[coll_name]
            item = dict(item)
            collection.insert_one(item)
