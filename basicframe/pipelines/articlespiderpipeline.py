import scrapy
from datetime import datetime
from scrapy.utils.project import get_project_settings
from basicframe.midwares.dbclient import DbClient


class ArticleSpiderPipeline:
    settings = get_project_settings()

    def open_spider(self, spider):
        self.db = DbClient(spider.settings['MONGO_URL'])
        self.db.change_table(spider.site_info['lang'])
        self.spider_logger = spider.spider_logger

    def process_item(self, item: scrapy.Item, spider):
        try:
            if len(item['content']) > 50:
                item = dict(item)
                print(item)
                self.db.put(item)
        except Exception as e:
            self.spider_logger.error(f"no content field {item}")
    def generate_name(self, str):
        now = datetime.now()
        time_str = now.strftime("%Y_%m_%d")
        return f"{str}_{time_str}"
