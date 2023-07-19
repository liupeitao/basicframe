import os

import redis
import requests

redis_conn = redis.Redis(host='106.15.10.74', port=6379, db=0, password='Liupeitao1.')


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
    file_name = name.replace(':', '_').replace('/', '_').replace('.','_')
    return file_name
    # return os.path.join(dir, file_name)


if __name__ == '__main__':
    save_dir = 'npr_song'
    while True:
        item = redis_conn.rpop('npr_filtered_test')
        item = eval(item)
        dir = os.path.join(save_dir, item['category'])
        mkdir(dir)
        file_name = generate_file_name(dir, item['url'])
        try:
            content = requests.get(item['url']).content
            save_song(content, file_name)
            save_subtitle(item['subtitle'], file_name)
        except Exception as e:
            redis_conn.lpush('npr_error', item)



