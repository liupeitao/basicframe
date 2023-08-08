import urllib

import pandas as pd

from basicframe.filters.filter import NetFilter
from basicframe.midwares.redisclient import RedisClient
redis_conn = RedisClient().connect()


    # df = pd.read_excel('/home/liupeitao/src/article-spiders-main/article_spider/spiders/xinyuan.xlsx', sheet_name=name).iloc[:, 2]
all_site_info = NetFilter().get_xinyuan_meta()
print(all_site_info)
    # for url in df:
    #
    #     if all_site_info[domain]['all']:
    #         with open('../assets/xinyuan.txt', mode='w') as f:
    #             f.write()
    #     else:
    #         pass

