import math
import multiprocessing
import socket
import time
import urllib
from urllib.parse import urlparse

import redis
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from basicframe.settings import REDIS_URL
from basicframe.spiders.fullsitespider import FullSiteSpider
from basicframe.spiders.genericspider import GenericSpider
from basicframe.utils.logHandler import LogHandler
from basicframe.utils.util import generate_std_name, current_date_time

redis_client = redis.from_url(REDIS_URL)

from basicframe.playground.sf import processor


def generate_name(url):
    return f"{generate_std_name(url)}_{current_date_time()}"


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
            'start_url': name,
        },
        'type': site_type,
        'name': name,
        'allowed_domains': [f'{urllib.parse.urlparse(name).netloc}'],
        'spider_logger': LogHandler(name=generate_name(name), file=True)
    }
    return args


def start_new_spider():
    doc = processor.fetch_random_one({"preprocess": True, "vpn_need": False, "type": "00", 'status': 'ready'})
    args = build_args(doc)
    doc['status'] = 'crawling'
    doc['start_crawling'] = current_date_time()
    doc['process_host'] = socket.gethostname()
    processor.update(doc)
    try:
        start_crawl_site(**args)
        update_finish_spider_status(doc)
        doc['message'] = 'exit ok'
    except Exception as e:
        doc['status'] = 'fatal'
        doc['message'] = str(e) + str(current_date_time())
    doc['end_crawling'] = current_date_time()
    processor.update(doc)


def restart_a_spider(doc):  # 重新启动中断过的爬虫
    args = build_args(doc)
    start_crawl_site(**args)


# def restart_all_spider(docs):  # 重新启动所有中断的爬虫
#     for doc in docs:
#         restart_a_spider(doc)


def get_all_crawling_spider():
    update_spiders_status()
    docs = processor.fetch(pipeline={'status': 'crawling'})
    return list(docs)


def crawling_spider_list_from_redis():
    spider_list = [key.decode() for key in redis_client.keys() if 'requests' in key.decode()]
    return spider_list


def finish_spider_list_from_redis():
    spider_list = [key.decode() for key in redis_client.keys() if 'dupefilter' in key.decode()]
    return spider_list


def update_spiders_status():
    try:  # 依据dupe队列数量更新状态,
        crawling_url_list = crawling_spider_list_from_redis()
        finish_url_list = finish_spider_list_from_redis()
        docs = processor.fetch(pipeline={'status': 'crawling'})
        for doc in docs:
            if f"{doc['start_url']}:requests" not in crawling_url_list and f"{doc['start_url']}:dupefilter" in finish_url_list:
                print(f"存在dup队列 无req队列 更新状态{doc['start_url']}")
                update_finish_spider_status(doc)
            else:
                print(f'$正在运行中 无法更新状态: {doc["start_url"]}')
                continue
    except Exception as e:
        # You can use logging or print to see the error.
        print(f"Error occurred while updating spider status: {e}")


def restart_all_spiders(docs):
    processes = []
    for doc in docs:
        process = multiprocessing.Process(target=restart_a_spider, args=(doc,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()


def requests_set_length():
    spider_list = crawling_spider_list_from_redis()
    for spider in spider_list:
        print(spider, redis_client.zcard(spider))


def get_finished_spiders():
    docs = processor.fetch(pipeline={'status': 'finish'})
    return list(docs)


def update_finish_spider_status(doc):
    dup_key = doc['start_url'] + ':dupefilter'
    req_key = doc['start_url'] + ':requests'
    dup_lens = redis_client.scard(dup_key)
    if dup_lens > 0:
        print("存在dupe不存在req队列:", doc)
    else:
        return
    if not redis_client.exists(req_key):
        if 0 < dup_lens < 100:
            doc['status'] = 'error'
        elif 150 < dup_lens < 300:
            doc['status'] = 'bug'
        elif 300 < dup_lens:
            doc['status'] = 'finish'
        doc['finish_time'] = current_date_time()
        doc['total'] = math.ceil(dup_lens * 0.75)
        processor.update(doc)


def judge_finish_bugs():
    spiders = get_finished_spiders()
    for spider in spiders:
        if spider['total'] != 0:
            continue
        dup_key = spider['start_url'] + ':dupefilter'
        req_key = spider['start_url'] + ':requests'
        dup_lens = redis_client.scard(dup_key)
        if dup_lens > 0:
            print(spider)
        else:
            continue
        if not redis_client.exists(req_key):
            if 0 < dup_lens < 100:
                spider['status'] = 'error'
            elif 150 < dup_lens < 300:
                spider['status'] = 'bug'
            elif 300 < dup_lens:
                spider['status'] = 'finish'
                spider['finish_time'] = current_date_time()
            spider['total'] = math.ceil(dup_lens * 0.90)
            processor.update(spider)


def run_spiders(num_spiders=None, max_total_spiders=100):
    if num_spiders is None:
        num_spiders = min(36, multiprocessing.cpu_count())  # 默认使用CPU核心数量

    started_spiders = 0  # 已启动的爬虫数量
    processes = []

    # 启动初始爬虫
    for index in range(num_spiders):
        if started_spiders < max_total_spiders:
            p = multiprocessing.Process(target=start_new_spider)
            p.start()
            processes.append(p)
            started_spiders += 1

    while started_spiders < max_total_spiders:
        # 检查每个进程，看它是否还在运行
        for index in range(len(processes)):
            if not processes[index].is_alive():
                # 如果进程不再运行，并且还没有达到历史最大任务数，则启动新的进程
                if started_spiders < max_total_spiders:
                    p = multiprocessing.Process(target=start_new_spider)
                    p.start()
                    processes[index] = p
                    started_spiders += 1
        time.sleep(60)  # 间隔30秒钟再次检查进程状态

    # 等待剩下的进程完成
    for p in processes:
        p.join()

    print("All tasks completed.")


if __name__ == '__main__':
    # for i in range(5):
    run_spiders()
    # update_spiders_status()

    # restart_all_spiders(get_all_crawling_spider())
