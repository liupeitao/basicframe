from tasks import get_m3u8_duration_task, down_m3u8_task, html_video_download_task
from basicframe.utils.htmlvideoutil import HtmlVideoUtil
from basicframe.midware.redisclient import RedisClient
redis_conn = RedisClient().connect()
item_list = redis_conn.lrange('not_down', 0, 5)

for item in item_list:
    item = item.decode()
    result = html_video_download_task.delay(item)
    print(result.id)

# 1 run command `celery -A tasks worker --loglevel=info` in cli
# 2 run this py file