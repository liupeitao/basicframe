# 格式化日志消息并记录
# logging.info(template.format(user=user, action=action))

"""
    继承Filter 重写do_filter方法， 即可添加一个过滤条件
    目前LanguageFilter 存在一些性能问题
"""
import json
import urllib.parse
from urllib.parse import urlparse

import pandas as pd
from langdetect import detect



def read_xlsx(path):
    df = pd.read_excel(path)
    return str(df.iloc[:, 2])


class Filter:
    def do_filter(self, m3u8_url, response, chain):
        response = m3u8_url
        return True

class NetFilter(Filter):
    def __init__(self):
        self.site_info_dict = None
        self.excel_file_path = '/home/ptking/多语种-文本-20230615.xlsx'
    def get_xinyuan_meta(self):
        if self.site_info_dict:
            return self.site_info_dict
        self.site_info_dict = {}
        excel_file = pd.ExcelFile(self.excel_file_path)
        sheet_names = excel_file.sheet_names
        for name in sheet_names:
            df = pd.read_excel(self.excel_file_path, sheet_name=name).iloc[:, 5]
            for url in df:
                if url is not str:
                    continue
                parsed_url = urllib.parse.urlparse(url)
                if parsed_url.path == '/':
                    url = parsed_url.netloc
                    self.site_info_dict[url] = {'all': True}
                else:
                    url = parsed_url.netloc
                    self.site_info_dict[url] = {'all': False, 'path': parsed_url.path}
                self.site_info_dict[url]['domain'] = name
        return self.site_info_dict

    def do_filter(self, url, response, chain):
        all_site_info = self.get_xinyuan_meta()
        domain = urllib.parse.urlparse(url).netloc
        try:
            if all_site_info[domain]['all']:
                return True
            else:
                return urllib.parse.urlparse(url).path.startswith(all_site_info[domain]['path']) or all_site_info[domain]['path'] in url or 'politics' in url or 'Politics' in url
        except KeyError as e :
            print("key eeorr... except", url)
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
    pass
