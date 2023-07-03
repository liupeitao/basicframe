import asyncio

from basicframe.utils.htmlvideoutil import HtmlVideoUtil
from basicframe.midware.redisclient import RedisClient
redis_conn = RedisClient().connect()

item_list = redis_conn.lrange('ru', 0, 1)
for item in item_list:
    item = eval(item)
    video = HtmlVideoUtil(path_id=item['url'], source='ru', save_dir='')
    video.download()
