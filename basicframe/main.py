import json
import urllib
from urllib.parse import urlparse

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from basicframe.midwares.dbclient import DbClient
from basicframe.settings import REDIS_URL
from basicframe.spiders.fullsitespider import FullSiteSpider
from basicframe.spiders.genericspider import GenericSpider
from basicframe.spiders.pspider import PenericSpider
from basicframe.utils.logHandler import LogHandler
from basicframe.utils.util import generate_std_name

redis_client = DbClient(REDIS_URL)


def generate_name(str):
    return f"{generate_std_name(str)}"


def start_scrapy(**kwargs):
    # 创建CrawlerProcess实例
    process = CrawlerProcess(get_project_settings())
    # 将爬虫添加到CrawlerProcess中
    process.crawl(GenericSpider, **kwargs)
    # 启动爬虫
    process.start()


def start_scrapy_full_site(start_url):
    process = CrawlerProcess(get_project_settings())
    # 将爬虫添加到CrawlerProcess中
    args = {
        'name': start_url,
        'allowed_domains': [f'{urllib.parse.urlparse(start_url).netloc}'],
        'spider_logger': LogHandler(name=f"crawling/{generate_name(start_url)}", file=True)
    }
    process.crawl(FullSiteSpider, **args)
    # 启动爬虫
    process.start()


def process_url(url):
    if '%' not in url:
        return url
    else:
        return url.replace('%', '%%')


def crawl_specific_url(**kwargs):
    start_scrapy(**kwargs)


def start_crawl_site(spider_cls, **kwargs):
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider_cls, **kwargs)
    # 启动爬虫
    process.start()

from basicframe.playground.sf import processor
from basicframe.feedstart import judb
from basicframe.midwares.dbclient import DbClient
db_client =DbClient('mongodb://root:root123456@106.15.10.74:27017/admin')

if __name__ == '__main__':
    # spider_type = [FullSiteSpider, GenericSpider]
    # # crawl_redis_url()
    # # crawl_specific_url('http://www.naewoeilbo.com/news/articleList.html?sc_section_code=S1N4&view_type=sm')
    # while True:
    #     siteinfo = db_client.get()
    #     start_url = siteinfo['start_url']
    #     if judb(start_url):
    #         break
    #     else:
    #         continue
    # args = {
    #     'site_info':{
    #     'domain': siteinfo['领域'],
    #     'sub_domain' : siteinfo['子领域'],
    #     'lang' : siteinfo['语种代码'],
    #     },
    #     'name': siteinfo['start_url'],
    #     'allowed_domains': [f'{urllib.parse.urlparse(start_url).netloc}'],
    #     'spider_logger': LogHandler(name=generate_name(start_url), file=True)
    # }
    # crawl_specific_url(**args)
    #

    name = 'https://www.foxsports.com/nba'
    args = {
        'site_info': {
            'domain': 'NBA',
            'lang': name+'2023_08_23',
        },
        'name': name,
        'allowed_domains': [f'{urllib.parse.urlparse(name).netloc}'],
        'spider_logger': LogHandler(name=generate_name(name), file=True)
    }
    start_crawl_site(PenericSpider, **args)
