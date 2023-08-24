import urllib.parse

from basicframe.midwares.dbclient import DbClient

from basicframe.settings import REDIS_URL, MONGO_URL
from basicframe.siteinfosettings import contains_substring, Partial_Static_Crawling as P_S_C
from basicframe.utils.peekurl import get_urls_from_page

mongo_client = DbClient(MONGO_URL)
redis_client = DbClient(REDIS_URL)


def send_start_to_redis_from_mongo():
    mongo_client.change_table('siteinfo')
    sites = mongo_client.get_all()
    for site in list(sites):
        id = site.pop('_id')
        goal = 0
        print("process url:", site['start_url'])
        url_list = get_urls_from_page(site['start_url'])
        for url in url_list:
            if contains_substring(url, P_S_C['page_allow_tuple']):
                goal += 1
        if goal >= 2:
            print("可以抓取")
            redis_client.update()

def send_start_from_url(store, raw_url):
    print("process url:", raw_url)
    goal = 0
    url_list = get_urls_from_page(raw_url)
    for url in url_list:
        if contains_substring(url, P_S_C['page_allow_tuple']):
            goal += 1
        if goal >= 2:
            print("可以抓取")
            return True
    return False




def judb(url):
    goal = 0
    print(url)
    url_list = get_urls_from_page(url)
    for url in url_list:
        if contains_substring(url, P_S_C['page_allow_tuple']):
            goal += 1
    if goal >= 2:
        print("可以抓取")
        return True
    return False

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
    nba_page = open('nba_page.txt', mode='a')
    with open('/home/ptking/basicframe/basicframe/playground/output.txt', mode='r') as f:
        for line in f:
            url = line.strip()
            if send_start_from_url('nba',url):
                nba_page.write(url+'\n')

