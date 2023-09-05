import scrapy
import datetime
from scrapy.utils.project import get_project_settings

import basicframe.settings
from basicframe.midwares.dbclient import DbClient


class ArticleSpiderPipeline:
    settings = get_project_settings()

    def open_spider(self, spider):
        self.db_client = DbClient(spider.settings['MONGO_URL'])
        self.db_client.change_db(
            f"{basicframe.settings.MONGO_DB}_{str(datetime.datetime.now().date())}")  # 每天都有新数据库， 手机前天的数据库。
        self.db_client.change_table(spider.site_info['lang'])
        self.spider_logger = spider.spider_logger

    def process_item(self, item: scrapy.Item, spider):
        try:
            if len(item['content']) > 50:
                item = dict(item)
                print(item)
                self.db_client.put(item)
        except KeyError as e:
            self.spider_logger.error(f"no content field {item}")
        except ConnectionError as e:
            self.spider_logger.error(f"can't insert to mongo network error mongo or server break down: {item}")
        except Exception as e:
            pass
