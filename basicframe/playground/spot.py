import os
import pprint
import json
import re
import urllib.parse

from gerapy_auto_extractor import is_detail, is_list, probability_of_detail, probability_of_list

import requests

proxies = {
    'http': 'http://localhost:7890',
    'https': 'http://localhost:7890'
}
def judge_list( url):
    html =  requests.get(url, proxies=proxies).text
    try:
        print(probability_of_detail(html), probability_of_list(html))
        if is_list( html):
            return 'list'
        else:
            return 'detail'

    except Exception as e:
        return None

def process_file(file_path):
    r = RedisClient().connect()
    list_urls = set()
    detail_urls = set()
    error_urls = set()
    res = {}
    with open(file_path, mode='r') as f:
        try:
            x = json.loads(f.readline())
        except Exception as e:
            return
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
        r.rsave_site_info_to_redis('网站url信息', 'https://www.cbsnews.com', **res )

from basicframe.midwares.redisclient import RedisClient
if __name__ == '__main__':
    process_file('/home/liupeitao/PycharmProjects/basicframe/basicframe/utils/test.txt')


#
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



