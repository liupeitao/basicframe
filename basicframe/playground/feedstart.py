from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from basicframe.test.logHandler import LogHandler
from basicframe.midwares.redisclient import RedisClient
from basicframe.siteinfosettings import contains_substring, page_substr_tuple
from basicframe.spiders.genericspider import GenericSpider
from basicframe.utils.get_url import get_urls_from_page

def send_start_to_redis():
    redis_client = RedisClient().connect()
    keys = redis_client.hgetall('网站信息')

    for key in keys:
        goal = 0
        print("process url:", key)
        key = key.decode()
        url_list = get_urls_from_page(key)
        for url in url_list:
            if contains_substring(url, page_substr_tuple):
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
        path= urlparse(url)
        if path == '/':
            print(True, url)

def start_scrapy(start_url):
    # 创建CrawlerProcess实例
    process = CrawlerProcess(get_project_settings())

    # 将爬虫添加到CrawlerProcess中
    process.crawl(GenericSpider, name=start_url)

    # 启动爬虫
    process.start()


def process_url(url):
    if '%' not in url:
        return url
    else:
        return url.replace('%', '%%')

if __name__ == '__main__':
    # redis_client = RedisClient().connect()
    # url = redis_client.lpop('静态部分网站')
    # logger = LogHandler(name='start_scrapy', file=True)
    # logger.info(f'start_scrapy ... {url}')

    # url = url.decode()
    url = 'http://www.hkbs.co.kr/news/articleList.html?sc_section_code=S1N3&view_type=sm'
    url = process_url(url)
    start_scrapy(url)
    # 某些网站需要重定向http://www.jjan.kr/news/articleList.html?sc_section_code=S1N31&view_type=sm