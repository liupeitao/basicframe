from basicframe.midwares.redisclient import RedisClient
from basicframe.utils.get_url import get_url_list

redis_client = RedisClient().connect()
keys = redis_client.hgetall('网站信息')
total = len(keys)
now = 0

for key in keys:
    print("process url:", key)
    key = key.decode()
    url_list = get_url_list(key)
    for url in url_list:
        if 'page' in url:
            print("可以抓取")
            main()



from scrapy import cmdline

def start_spider(start_url):
    # 构造命令行参数
    argv = ['scrapy', 'crawl', 'spider_name', '-a', f'start_url={start_url}']
    # 调用命令行执行scrapy命令
    cmdline.execute(argv)

# 通过外界传入的URL启动爬虫
start_url = 'http://www.example.com'
start_spider(start_url)