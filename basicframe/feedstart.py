import urllib.parse
from datetime import datetime

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from basicframe.midwares.redisclient import RedisClient
from basicframe.siteinfosettings import contains_substring, Partial_Static_Crawling as P_S_C
from basicframe.spiders.fullsitespider import FullSiteSpider
from basicframe.spiders.genericspider import GenericSpider
from basicframe.utils.logHandler import LogHandler
from basicframe.utils.peekurl import get_urls_from_page
from basicframe.utils.util import generate_std_name, current_date_time


# def generate_name(str):
#     return f"{current_date_time()}_{generate_std_name(str)}"

from basicframe.midwares.mongodbclient import MongoDBClient

def send_start_to_redis_from_mongo():
    redis_client = RedisClient().connect()
    mongo_client = MongoDBClient()
    sites = mongo_client.get_address_values('articel', 'siteinfo', '地址')
    for site in sites:
        goal = 0
        print("process url:", site)
        url_list = get_urls_from_page(site)
        for url in url_list:
            if contains_substring(url, P_S_C['page_allow_tuple']):
                goal += 1
        if goal >= 4:
            print("可以抓取")
            redis_client.lpush("欧冠", site)


def send_start_to_redis():
    redis_client = RedisClient().connect()
    keys = redis_client.hgetall('网站信息')

    for key in keys:
        goal = 0
        print("process url:", key)
        key = key.decode()
        url_list = get_urls_from_page(key)
        for url in url_list:
            if contains_substring(url, P_S_C['page_allow_tuple']):
                goal += 1
        if goal >= 2:
            print("可以抓取")
            redis_client.lpush("静态部分网站", key)


from urllib.parse import urlparse


def is_full():
    redis_client = RedisClient().connect()
    keys = redis_client.hgetall('网站信息')
    for key in keys:
        # print("process url:", key)
        key = key.decode()
        url = key
        path = urlparse(url)
        if path == '/':
            print(True, url)


# def start_scrapy(start_url):
#     # 创建CrawlerProcess实例
#     process = CrawlerProcess(get_project_settings())
#     # 将爬虫添加到CrawlerProcess中
#     args = {
#         'name': start_url,
#         'allowed_domains': [f'{urllib.parse.urlparse(start_url).netloc}'],
#         'spider_logger': LogHandler(name=generate_name(start_url), file=True)
#     }
#     process.crawl(GenericSpider,  **args)
#     # 启动爬虫
#     process.start()
#
#
#
# def start_scrapy_full_site(start_url):
#     # 创建CrawlerProcess实例
#     process = CrawlerProcess(get_project_settings())
#     # 将爬虫添加到CrawlerProcess中
#     args = {
#         'name': start_url,
#         'allowed_domains': [f'{urllib.parse.urlparse(start_url).netloc}'],
#         'spider_logger': LogHandler(name=generate_name(start_url), file=True)
#     }
#     process.crawl(FullSiteSpider,  **args)
#     # 启动爬虫
#     process.start()
#
# def process_url(url):
#     if '%' not in url:
#         return url
#     else:
#         return url.replace('%', '%%')
#
#
# def crawl_specific_url(url):
#     url = process_url(url)
#     start_scrapy(url)
#
#
# def crawl_redis_url():
#     redis_client = RedisClient().connect()
#     url = redis_client.lpop('静态部分网站').decode()
#     logger = LogHandler(name='start_scrapy', file=True)
#     logger.info(f'start_scrapy ... {url}')
#     crawl_specific_url(url)
#




if __name__ == '__main__':
    send_start_to_redis_from_mongo()
    # start_scrapy_full_site('https://www.spacewar.com/')
    # url = 'https://en.as.com/news/champions-league/'
    # crawl_specific_url(url)
