import urllib

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from basicframe.midwares.redisclient import RedisClient
from basicframe.spiders.fullsitespider import FullSiteSpider
from basicframe.spiders.genericspider import GenericSpider
from basicframe.utils.logHandler import LogHandler
from basicframe.utils.util import current_date_time, generate_std_name


def generate_name(str):
    return f"{generate_std_name(str)}"


def start_scrapy(start_url):
    # 创建CrawlerProcess实例
    process = CrawlerProcess(get_project_settings())
    # 将爬虫添加到CrawlerProcess中
    args = {
        'name': start_url,
        'allowed_domains': [f'{urllib.parse.urlparse(start_url).netloc}'],
        'spider_logger': LogHandler(name=generate_name(start_url), file=True)
    }
    process.crawl(GenericSpider, **args)
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


def crawl_specific_url(url):
    url = process_url(url)
    start_scrapy(url)


def crawl_redis_url():
    redis_client = RedisClient().connect()
    url = redis_client.lpop('欧冠').decode()
    logger = LogHandler(name='start_scrapy', file=True)
    logger.info(f'start_scrapy ... {url}')
    crawl_specific_url(url)


def start_crawl_site(spider_type, start_url):
    process = CrawlerProcess(get_project_settings())
    # 将爬虫添加到CrawlerProcess中
    args = {
        'name': start_url,
        'allowed_domains': [f'{urllib.parse.urlparse(start_url).netloc}'],
        'spider_logger': LogHandler(name=f'crawling/{generate_name(start_url)}', file=True)
    }
    process.crawl(spider_type, **args)
    # 启动爬虫
    process.start()




if __name__ == '__main__':
    spider_type = [FullSiteSpider, GenericSpider]
    # crawl_redis_url()
    start_crawl_site(FullSiteSpider, 'https://www.skysports.com/nba/news')
    # crawl_specific_url('https://www.sportskeeda.com/go/serie-a-calcio/news')
    # crawl_specific_url('https://www.dailymail.co.uk/sport/copa_america/index.html')

    # https: // www.cricketworldcup.com /