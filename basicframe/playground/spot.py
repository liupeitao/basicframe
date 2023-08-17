import requests
from gerapy_auto_extractor import is_list, probability_of_detail, probability_of_list, is_detail

from basicframe.utils.logHandler import LogHandler

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





