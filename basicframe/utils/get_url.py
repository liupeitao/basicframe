import subprocess
from basicframe.test.logHandler import LogHandler


def get_urls_from_page(page_url):
    logger = LogHandler(name='urlfinder', file=True)
    ret = subprocess.run(
        args=['urlfinder', '-x', 'http://127.0.0.1:7890', '-u', page_url],
        stdout=subprocess.PIPE)
    try:
        url_list = ret.stdout.decode('utf-8')
    except UnicodeDecodeError as e:
        logger.error(f"{page_url} {e} url can't decode by utf-8")
        return []

    try:
        url_list = url_list.split('URL to')[1]
    except IndexError as e:
        logger.error(f"{page_url} {e} urls urlfinder return isn't enough")
        return []

    res = []
    for url in url_list.split('\n'):
        res.append(url)

    return list(set(res))
