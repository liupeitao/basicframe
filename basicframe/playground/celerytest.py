from basicframe.midwares.redisclient import RedisClient
from tasks import html_video_download_task

redis_conn = RedisClient().connect()
item_list = redis_conn.lrange('not_down', 0, 5)

for item in item_list:
    item = item.decode()
    result = html_video_download_task.delay(item)
    print(result.id)
    
# 1 run command `celery -A tasks worker --loglevel=info` in cli
# 2 run this py file