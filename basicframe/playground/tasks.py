import json
import random
import time

import requests

from basicframe.midwares.celeryclient import app
from basicframe.midwares.mongodbclient import MongoDBClient
from basicframe.spiders.extractors.articelextractor import extractor_articel_gen
mongo = MongoDBClient().connect()['article']['tridetail']
from basicframe.midwares.redisclient import RedisClient
redis_conn = RedisClient().connect()
from basicframe.utils.logHandler import LogHandler
logger = LogHandler(name='catch_news', file=True)
proxy_list = []
request_count = 1

def get_proxy_list():
    global proxy_list
    try:
        ip_port_list = requests.get("https://servers.qunyindata.com/GetWDProxy?count=50").json()["results"]
        proxys = [f'http://{ip_port}' for ip_port in ip_port_list]
        proxy_list = proxys
    except Exception as e:
        print("Failed to fetch proxy list:", str(e))

def get_random_proxy():
    global request_count
    if request_count % 30 == 0:
        request_count = 1
        get_proxy_list()  # 更新代理池
    if not proxy_list:
        get_proxy_list()  # 初始化代理池
    request_count += 1
    return random.choice(proxy_list)

@app.task(queue='processurls', ignore_result=True)
def news_processing_article(news_info):
    redis_coll = 'detailurls'
    site_info = {
        'domains': ''
    }
    try:
        proxy = get_random_proxy()
        response = requests.get(news_info['url'], proxies={"http": proxy, "https": proxy}, timeout=100)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except (requests.RequestException, Exception) as e:
        logger.info(f"downloading error: {news_info['url']}")
        redis_conn.lpush(redis_coll, news_info['url'])
        return None
    try:
        news_data = extractor_articel_gen(response, site_info)
        if len(news_data.get('content', '')) > 50:
            logger.info(news_info['url'])
            mongo.insert_one(dict(news_data))
            print(news_data)
            return news_data
    except Exception as e:
        logger.warning(f"jiexishibai: {news_info['url']}")
        # Handle extraction errors separately if needed
        redis_conn.lpush(redis_coll, news_info['url'])
        return None
    return None



from lxml import html


@app.task(queue='news_processing_queue')
def tripagetodetail(url, base_url):
    detail_urls = []
    try:
        response = requests.get(url, timeout=30)
    except Exception:
        return []
    if response.status_code != 200:
        return []
    content = response.content
    tree = html.fromstring(content)

    # 使用lxml解析HTML获取详情页URL
    page_urls = tree.xpath('//*[@class="grid__item palm-one-half desk-wide-one-third"]//a/@href')
    # 拼接完整URL
    detail_urls.extend(['https://www.tribalfootball.com' + page_url for page_url in page_urls])
    print(detail_urls)
    return detail_urls

# @app.task(queue='urltomongo')
# def tripagetodetail(url):
#     detail_urls = []
#     try:
#         response = requests.get(url, timeout=30)
#     except Exception:
#         return []
#     if response.status_code != 200:
#         return []
#     content = response.content
#     tree = html.fromstring(content)
#
#     # 使用lxml解析HTML获取详情页URL
#     page_urls = tree.xpath('//*[@class="grid__item palm-one-half desk-wide-one-third"]//a/@href')
#     # 拼接完整URL
#     detail_urls.extend(['https://www.tribalfootball.com' + page_url for page_url in page_urls])
#     print(detail_urls)
#     return detail_urls