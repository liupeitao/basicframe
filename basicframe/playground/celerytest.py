import json

from basicframe.playground.tasks import news_processing_article, tripagetodetail

from pathlib2 import Path

# src_file = Path('../assets/2023_0815_待提交_politico_file.txt')
# res = open('../2023_0815_待提交_politico_file.json', mode='w')
# with src_file.open() as f:
#     for line in f:
#         line = line.strip()
#         item = {
#             'url': line,
#             'domain': "政治"
#         }
#         # item = dict(json.loads(line))
#         # item['url'] = item['url'].replace(' ', '')
#         r = news_processing_article.delay(item)
#         res.write(r.id+'\n')
from basicframe.midwares.redisclient import RedisClient
redic_conn = RedisClient().connect()
if __name__ == '__main__':

    while True:
        try:
            url = redic_conn.rpop('tripage')
            url = url.decode()
            task = tripagetodetail.apply_async(args=([url, 'https://www.tribalfootball.com']))
            result = task.get()
            if result is None or len(result) == 0:
                redic_conn.lpush('tripage', url)
                print('差回去')
            else:
                print("输出第一个代表", result[0])
                for url in result:
                    redic_conn.lpush('detailurls', url)
        except Exception as e:
            print(e)
            break



