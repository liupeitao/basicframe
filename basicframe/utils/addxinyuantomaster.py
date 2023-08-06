import urllib

import pandas as pd

from basicframe.filters.filter import NetFilter
from basicframe.midwares.redisclient import RedisClient
redis_conn = RedisClient().connect()

sheet_names = ['发布会']
for name in sheet_names:
    df = pd.read_excel('/home/liupeitao/src/article-spiders-main/article_spider/spiders/xinyuan.xlsx', sheet_name=name).iloc[:, 2]
    for url in df:
        all_site_info = NetFilter().get_xinyuan_meta()
        domain = urllib.parse.urlparse(url).netloc
        if all_site_info[domain]['all']:
            redis_conn.lpush('article_spider:start_urls', url)
        else:
            pass

