from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from basicframe.midwares.redisclient import RedisClient
from basicframe.spiders.genericspider import GenericSpider
from basicframe.utils.get_url import get_url_list


def send_start_to_redis():
    redis_client = RedisClient().connect()
    keys = redis_client.hgetall('网站信息')
    for key in keys:
        print("process url:", key)
        key = key.decode()
        url_list = get_url_list(key)
        for url in url_list:
            if 'page' in url:
                print("可以抓取")
                redis_client.lpush("静态部分网站", key)
                break

def start_scrapy(start_url):
    # 创建CrawlerProcess实例
    process = CrawlerProcess(get_project_settings())

    # 将爬虫添加到CrawlerProcess中
    process.crawl(GenericSpider, name=start_url)

    # 启动爬虫
    process.start()



if __name__ == '__main__':

    redis_client = RedisClient().connect()
    url = redis_client.rpop("静态部分网站")
    url = url.decode()
    if '%' in url:
    # url = 'https://terms.naver.com/list.naver?cid=50280&categoryId=50280&so=st3.asc&viewType=&categoryType=&index=%E3%84%B7'
        url = url.replace('%', '%%')
        # print("==================", r'{url}')
    start_scrapy(url)



