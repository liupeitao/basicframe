# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import pymongo
from scrapy.utils.project import get_project_settings
from basicframe.midwares.mongodbclient import mongo_client
class ArticleSpiderPipeline:
    settings = get_project_settings()

    def __init__(self):
        # host = self.settings['MONGODB_HOST']
        # port = self.settings['MONGODB_PORT']
        # user = self.settings['MONGODB_USER']
        # passwd = self.settings['MONGODB_PASSWD']
        dbName = self.settings['MONGO_DB']
        coll = self.settings['MONGO_COLL']
        dbx = mongo_client[dbName]
        self.post = dbx[coll]

    def process_item(self, item, spider):
        carinfo = dict(item)
        print(carinfo)

        self.post.insert_one(carinfo)

