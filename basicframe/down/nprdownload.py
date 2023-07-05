import os
import requests
from concurrent.futures import ThreadPoolExecutor
from basicframe.midware.redisclient import RedisClient
redis_conn = RedisClient().connect()
def save_subtitle(subtitle, path):
    with open(f'{path}.txt', mode='w') as f:
        f.write(subtitle)
def save_song(content, path):
    with open(f'{path}.mp3', mode='wb') as f:
        f.write(content)

def mkdir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
def generate_file_name(dir, name):
    file_name = name.replace(':', '_').replace('/', '_').replace('.', '_')
    return os.path.join(dir, file_name)

def process(item):
    item = eval(item)
    print("process", item['url'], item['title'])
    dir = os.path.join(save_dir, item['category'])
    mkdir(dir)
    file_name = generate_file_name(dir, item['url'])
    try:
        content = requests.get(item['url']).content
        save_song(content, file_name)
        save_subtitle(item['subtitle'], file_name)
    except Exception as e:
        redis_conn.lpush('npr_error', item)
        pass

if __name__ == '__main__':
    save_dir = '/media/ptking/Elements/en/npr'
    item_list = redis_conn.lrange('npr_filtered___1', 0, -1)
    pool = ThreadPoolExecutor(max_workers=10)
    for item in item_list:
        pool.submit(process, item)
    pool.shutdown()



