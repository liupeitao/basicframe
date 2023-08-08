import urllib

import pandas as pd

from basicframe.filters.filter import NetFilter
from basicframe.midwares.redisclient import RedisClient
# redis_conn = RedisClient().connect()

sheet_names = ['文本扒取-政治']
for name in sheet_names:
    df = pd.read_excel('/home/ptking/xinyuan.xlsx', sheet_name=name).iloc[:, 2]
    for url in df:
        with open('../assets/xinyuan.txt', mode='a') as f:
            f.write(f'{url}\n')


