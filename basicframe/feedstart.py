import urllib.parse

from basicframe.midwares.dbclient import DbClient

from basicframe.settings import REDIS_URL, MONGO_URL
from basicframe.siteinfosettings import contains_substring, Partial_Static_Crawling as P_S_C
from basicframe.utils.peekurl import get_urls_from_page

mongo_client = DbClient(MONGO_URL)
redis_client = DbClient(REDIS_URL)


def send_start_to_redis_from_mongo():
    redis_client.change_table('欧冠')
    mongo_client.change_table('siteinfo')
    sites = mongo_client.get_all()
    for site in sites:
        site.pop('_id')
        site['start_url'] = site['地址']
        goal = 0
        print("process url:", site['地址'])
        url_list = get_urls_from_page(site['地址'])
        for url in url_list:
            if contains_substring(url, P_S_C['page_allow_tuple']):
                goal += 1
        if goal >= 4:
            print("可以抓取")
            redis_client.put(site)


def is_full():
    redis_client.change_table('静态部分网站')
    keys = redis_client.get_all()
    for key in keys:
        # print("process url:", key)
        key = key.decode()
        url = key
        path = urllib.parse.urlparse(url)
        if path == '/':
            print(True, url)





if __name__ == '__main__':
    # send_start_to_redis_from_mongo()
    # is_full()
    pass
