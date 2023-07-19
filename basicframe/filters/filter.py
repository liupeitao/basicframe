# 格式化日志消息并记录
# logging.info(template.format(user=user, action=action))

"""
    继承Filter 重写do_filter方法， 即可添加一个过滤条件
    目前LanguageFilter 存在一些性能问题
"""
import json
from urllib.parse import urlparse

import pandas as pd
from langdetect import detect
from basicframe.utils.log import get_logger
from tqdm import tqdm

logger = get_logger('lw.txt')

def read_xlsx(path):
    df = pd.read_excel(path)
    return str(df.iloc[:, 2])


class Filter:
    def do_filter(self, m3u8_url, response, chain):
        response = m3u8_url
        return True


class LanguageFilter(Filter):
    def __init__(self, lang):
        self.lang = lang

    def do_filter(self, request, response, chain):
        try:
            if detect(request['content']) == 'en':
                return chain.do_filter(request, response)
            else:
                logger.error(f"不是英语: {line.strip()}")
                return False
        except Exception as e:
            return False


class XinYuanFilter(Filter):
    def __init__(self, xinyuan):
        self.xinyuan = xinyuan

    def do_filter(self, request, response, chain):
        parsed_url = urlparse(request['url'])
        domain = parsed_url.netloc
        if domain in self.xinyuan:
            return chain.do_filter(request, response)
        else:
            logger.error(f"不是信源里的: {line.strip()}")
            return False


class FilterChain:
    def __init__(self):
        self.filters = []
        self.index = 0

    def add_filter(self, filter):
        self.filters.append(filter)

    def do_filter(self, request, response):
        if self.index == len(self.filters):
            return True
        filter = self.filters[self.index]
        self.index += 1
        return filter.do_filter(request, response, self)


def process_line(line, chain: FilterChain):
    pass


def save_line(line, path):
    with open(path, mode='a') as f:
        f.write(line)


if __name__ == '__main__':
    file = '/media/ptking/Elements/en.json'
    xinyuan = '/home/ptking/xinyuan.xlsx'
    lang_filter = LanguageFilter('en')
    url_filter = XinYuanFilter(read_xlsx(xinyuan))
    filter_chain = FilterChain()
    filter_chain.add_filter(url_filter)
    filter_chain.add_filter(lang_filter)

    with open(file, mode='r') as f:
        f.seek(0)
        for index, line in tqdm(enumerate(f), total=10082988):
            line_jsonfy = json.loads(line)
            if filter_chain.do_filter(line_jsonfy, '2'):
                save_line(line, f"eng/{line_jsonfy['domain']}.txt")
            else:
                pass
            filter_chain.index = 0
