import json
from difflib import SequenceMatcher

from basicframe.midwares.redisclient import RedisClient
from basicframe.utils.get_url import get_urls_from_page


def likely_url_groups(url_list, threshold) -> dict:
    link_groups = {}  # 链接组字典
    for link in url_list:
        added_to_group = False
        for group_link in link_groups.keys():
            similarity = SequenceMatcher(None, link, group_link).ratio()
            if similarity >= threshold:
                link_groups[group_link].append(link)
                added_to_group = True
                break
        if not added_to_group:
            link_groups[link] = [link]
    return link_groups





def process_one_url(url, f, threshold = 0.90):
    url_list = get_urls_from_page(url)
    if not url_list:
        f.write(url)
        return
    url_list = list(set(url_list))
    #
    # 打印链接组
    # 阈值，用于确定链接的相似度阈值
    link_groups = likely_url_groups(url_list, threshold)
    f.write(json.dumps(link_groups))

def print_url_info(link_groups: dict):
    for group, group_links in link_groups.items():
        if len(group_links) > 1:
            print("group:")
            for link in group_links:
                print(link)


if __name__ == '__main__':
    pass
    # redis_client = RedisClient().connect()
    # keys = redis_client.hgetall('网站信息')
    # for key in keys:
    #     key = key.decode()
    #     file_name = f"{key.replace('/', '_').replace(':', '_').replace('.', '_')}.txt"
    #     with open(f'../assets/urlinfo/{file_name}', mode='w') as f:
    #         process_one_url(key, f, 0.9)

    # with open('test.txt', mode='w') as f:
    #     process_one_url('https://www.cbsnews.com', f)
    # start_url = 'https://www.tuttosport.com/search?q=ucl'
    # link_groups = likely_url_groups(get_url_list(start_url), 0.96)
    # print_url_info(link_groups)
    # url_list = get_url_list(start_url)
    #
    # for url in url_list:
    #     if url.startswith(start_url):
    #         print(url)