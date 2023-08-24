from urllib.parse import urlparse

from basicframe.siteinfosettings import Partial_Static_Crawling as P_S_C
from basicframe.siteinfosettings import contains_substring
from basicframe.utils.logHandler import LogHandler
from basicframe.utils.peekurl import get_urls_from_page


def judge_psp_type(raw_url):
    print("process url:", raw_url)
    goal = 0
    url_list = get_urls_from_page(raw_url)
    for url in url_list:
        if contains_substring(url, P_S_C['page_allow_tuple']):
            print(url, 'is page type')
            goal += 1
        if goal >= 2:
            logger = LogHandler(name='ps_type', file=True)
            logger.info(f'ps type {raw_url}')
            return True
    return False


def judge_full_type(raw_url):
    path = urlparse(raw_url).path
    if path == '' or path == '/':
        return True
    return False


class Filter:
    def do_filter(self, request, response, filter_chain):
        pass



class PartialStaticPageSiteFilter(Filter):
    def do_filter(self, request, response, filter_chain):
        if judge_psp_type(request):
            return 'psp_type'  # 00
        return filter_chain.do_filter(request, response)


class FullSiteFilter(Filter):
    def do_filter(self, request, response, filter_chain):
        if judge_full_type(request):
            return 'full_type'  # 10
        return filter_chain.do_filter(request, response)

class FilterChain:
    def __init__(self):
        self.filters = []
        self.index = 0

    def add_filter(self, filter):
        if not isinstance(filter, Filter):
            raise ValueError("Provided object is not a valid Filter")
        self.filters.append(filter)
        return self  # 返回self允许方法链式调用

    def do_filter(self, request, response):
        if self.index == len(self.filters):
            return False    # unknow type  in now
        filter = self.filters[self.index]
        self.index += 1
        return filter.do_filter(request, response, self)

    def reset(self):
        self.index = 0


chain = FilterChain().add_filter(FullSiteFilter()).add_filter(PartialStaticPageSiteFilter())

def judge_type(raw_url):
    res = chain.do_filter(raw_url, None)
    chain.reset()
    return res
if __name__ == '__main__':
    for i in range(10):
        print(judge_type('https://www.focus.de/immobilien/immobilienboerse/'))