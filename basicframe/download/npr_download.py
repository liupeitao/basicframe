import json
import re
import requests
from concurrent.futures import ThreadPoolExecutor
from basicframe.midwares.redisclient import RedisClient
redis_conn = RedisClient().connect()

def filte_item(item):
    item = eval(item)
    # subtitle = ','.join(item['subtitle'])
    response = requests.get(item['url'])
    try:
        mp3_url = re.findall(r'href="(.*mp3)', response.text)[0]
        text = item['subtitle']
        text = ','.join(text)
        if '.mp3' in mp3_url and len(text) > 100:
            item['url'] = mp3_url
            item['subtitle'] = text
            redis_conn.lpush('npr_filtered___1', json.dumps(item))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    item_list = redis_conn.lrange('npr_broadercast_teee', 0, -1)
    pool = ThreadPoolExecutor(max_workers=15)
    for item in item_list:
        pool.submit(filte_item, item)
    pool.shutdown()

    print("All tasks complete")
