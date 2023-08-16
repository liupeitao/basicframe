import urllib.parse
from datetime import datetime

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from basicframe.midwares.redisclient import RedisClient
from basicframe.siteinfosettings import contains_substring, Partial_Static_Crawling as P_S_C
from basicframe.spiders.genericspider import GenericSpider
from basicframe.utils.logHandler import LogHandler
from basicframe.utils.peekurl import get_urls_from_page
from basicframe.utils.util import generate_std_name, current_date_time


def generate_name(str):
    return f"{current_date_time()}_{generate_std_name(str)}"

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
        if goal >= 4:
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


def start_scrapy(start_url):
    # 创建CrawlerProcess实例
    process = CrawlerProcess(get_project_settings())
    # 将爬虫添加到CrawlerProcess中
    args = {
        'name': start_url,
        'allowed_domains': [f'{urllib.parse.urlparse(start_url).netloc}'],
        'spider_logger': LogHandler(name=generate_name(start_url), file=True)
    }
    process.crawl(GenericSpider,  **args)
    # 启动爬虫
    process.start()


def process_url(url):
    if '%' not in url:
        return url
    else:
        return url.replace('%', '%%')


def crawl_specific_url(url):
    url = process_url(url)
    start_scrapy(url)


def crawl_redis_url():
    redis_client = RedisClient().connect()
    url = redis_client.lpop('静态部分网站').decode()
    logger = LogHandler(name='start_scrapy', file=True)
    logger.info(f'start_scrapy ... {url}')
    crawl_specific_url(url)





if __name__ == '__main__':
    crawl_specific_url('https://terms.naver.com/list.naver?cid=43702&categoryId=43702&so=st3.asc&viewType=&categoryType=&index=%E3%85%8D')
    # crawl_redis_url()
    # url = 'https://en.as.com/news/champions-league/'
    # crawl_specific_url(url)
