import urllib
from urllib.parse import urlparse

import redis
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from basicframe.midwares.dbclient import DbClient
from basicframe.settings import REDIS_URL
from basicframe.spiders.fullsitespider import FullSiteSpider
from basicframe.spiders.genericspider import GenericSpider
from basicframe.utils.logHandler import LogHandler
from basicframe.utils.util import generate_std_name

redis_client = redis.from_url(REDIS_URL)


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


def start_crawl_site(**kwargs):
    process = CrawlerProcess(get_project_settings())
    print(kwargs['type'])
    if kwargs['type'] == '00':  # 部分爬取  有分页静态网站
        process.crawl(GenericSpider, **kwargs)
    elif kwargs['type'] == '10':  # 全站爬取 按照静态处理
        process.crawl(FullSiteSpider, **kwargs)
    elif kwargs['type'] == '11':  ## 部分爬取 动态类型网站
        pass
    elif kwargs['type'] == '12':  # 部分爬取， 类似于 /a/category1 /a/category2 ... /a/category1/detail_page.html
        pass
    # 启动爬虫
    process.start()


from basicframe.playground.sf import processor
from basicframe.midwares.dbclient import DbClient



mongo_client = DbClient('mongodb://root:root123456@106.15.10.74:27017/admin')


def build_args(doc):
    name = doc['start_url']
    lang = doc['语种']
    domain = doc["领域"]
    sub_domain = doc['子领域']
    site_type = doc['type']
    args = {
        'site_info': {
            'domain': domain,
            'sub_domain': sub_domain,
            'lang': lang,
        },
        'type': site_type,
        'name': name,
        'allowed_domains': [f'{urllib.parse.urlparse(name).netloc}'],
        'spider_logger': LogHandler(name=generate_name(name), file=True)
    }
    return args


def start_new_spider():
    doc = processor.fetch_one(pipeline={"preprocess": True, "type": "00", 'status': 'ready'})
    args = build_args(doc)
    doc['status'] = 'crawling'
    processor.update(doc)
    start_crawl_site(**args)


def restart_a_spider(doc):  # 重新启动中断过的爬虫
    # doc = processor.fetch_one(pipeline={"start_url": url})
    args = build_args(doc)
    start_crawl_site(**args)


def get_all_crawling_spider():
    docs = processor.fetch(pipiline={'status': 'crawling'})
    return list(docs)


def restart_all_spider(start_urls):  # 重新启动所有中断的爬虫
    for url in start_urls:
        restart_a_spider(url)


def requests_set_length():
    keys = redis_client.keys()
    for key in keys:
        key = key.decode()
        if 'requests' in key:
            print(key)
            print(redis_client.zcard(key))
        else:
            continue

if __name__ == '__main__':
    # restart_a_spider('https://famashow.pt/famosos')
    # restart_all_spider(get_all_crawling_spider())
    jiankong_()
