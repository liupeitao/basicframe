import pandas as pd

from basicframe.midwares.redisclient import RedisClient
redis_conn = RedisClient().connect()

sheet_names = ['政治', '发布会']
for name in sheet_names:
    df = pd.read_excel('/home/liupeitao/src/article-spiders-main/article_spider/spiders/xinyuan.xlsx', sheet_name=name).iloc[:, 2]
    for url in df:
        redis_conn.lpush('article_spider:start_urls', url)
