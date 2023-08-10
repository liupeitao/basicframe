import re

import requests
from gerapy_auto_extractor import is_list, probability_of_detail, probability_of_list, is_detail

from basicframe.test.logHandler import LogHandler
from basicframe.utils.get_url import get_urls_from_page

proxies = {
    'http': 'http://localhost:7890',
    'https': 'http://localhost:7890'
}
def judge_list(url):
    log = LogHandler('urljudge', file=True)
    html = requests.get(url, proxies=proxies).text
    try:
        print(probability_of_detail(html), probability_of_list(html))
        if is_list(html):
            return 'list'
        else:
            return 'detail'
    except Exception as e:
        log.warning(f'{url} Exception: {e} judge error')
        return None

def judge_list_by_html(html):
    if is_list(html):
        return probability_of_list(html)
    else:
        return 0

def judge_detail_by_html(html):
    if is_detail(html):
        return probability_of_detail(html)
    else:
        return 0

##  返回可能是 列表页和详情页
def process(url_meta):
    if not url_meta:
        return
    x = url_meta

    r = RedisClient().connect()
    list_urls = set()
    detail_urls = set()
    error_urls = set()
    res = {}

    for url in x.keys():
        if re.search(pattern='.jpg|png', string=url):
            continue
        if not url.startswith('http'):
            continue
        res = judge_list(url)
        if res == 'list':
            list_urls.add(url)
            print("list page", url)
        elif res == 'detail':
            detail_urls.add(url)
        else:
            error_urls.add(url)
    res['list_urls'].add(list_urls)
    res['detail_urls'] = detail_urls
    res['error_urls'] = error_urls
    # r.rsave_site_info_to_redis('网站url信息', 'https://www.cbsnews.com', **res )

from basicframe.midwares.redisclient import RedisClient
if __name__ == '__main__':
    # start_url = 'https://www.bbc.com/sport/football/champions-league/'
    # url_list = get_url_list(start_url)
    # url_meta = likely_url_groups(url_list, 0.7)




    redis_client = RedisClient().connect()
    keys = redis_client.hgetall('网站信息')
    total = len(keys)
    now = 0
    f = open('res.txt', mode='w')
    for key in keys:
        print("process url:", key)
        f.write("process url:" + str(key))
        key = key.decode()
        url_list = get_urls_from_page(key)
        for url in url_list:
            if 'page' in url:
                now += 1
                print(url)
                f.write(url+'\n')
        print("===============================================\n\n\n\n")
        f.write("===============================================\n\n\n\n")

    print(total, now)
    f.write(str(total) + "   " + str(now))

# import os
# dir = '/home/liupeitao/PycharmProjects/basicframe/basicframe/assets/urlinfo'
# for file in os.listdir(dir):
#     print("process_file:", file)
#     with open(os.path.join(dir, file), mode='r') as f:
#         try:
#             x = json.loads(f.readline())
#         except Exception as e:
#             continue
#         for url in x.keys():
#             if re.search(pattern='.jpg|png', string=url):
#                 continue
#             if not url.startswith('http'):
#                 continue
#             res = judge_list(url)
#             if res == 'list':
#                 print("list page", url)
#             else:
#                 pass
#     print("---------------------------------------------next")



