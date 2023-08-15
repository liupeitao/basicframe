import urllib.parse

import scrapy
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import Rule, CrawlSpider

from basicframe.spiders.extractors.articelextractor import extractor_articel
from basicframe.test.logHandler import LogHandler
from basicframe.utils.util import generate_std_name

recent_urls_set = set()
# 适用于部分分页。会有一点误差。
class GenericSpider(CrawlSpider):
    # name = 'http://www.enewstoday.co.kr/news/articleList.html?sc_section_code=S1N63&view_type=sm'
    # name = ''

    site_info = {'domains': '政治'}
    rules = (
        Rule(LinkExtractor(allow=('page=', '&page', 'page/\\d+')),
             callback='parse_item', follow=False, process_links='page_links'),
        Rule(LinkExtractor(),
             callback='parse_item', follow=False, process_links='custom_process_links'),
    )
    def page_links(self, links):
        return links


    def start_requests(self):
        yield scrapy.Request(self.name)

    def process_page_request(self, request: scrapy.Request):
        request.priority = 2  # 越大月高
        return request

    def custom_process_links(self, links):
        processed_urls = self.not_recent_processed_links(links)
        return processed_urls
    def parse_item(self, response: HtmlResponse):
        yield extractor_articel(response, self.site_info)

    def parse_page(self, response):
        pass

    def parse_all(self, response: HtmlResponse):
        pass


    @staticmethod
    def not_recent_processed_links(links):
        ok_links = []
        for link in links:
            if link.url not in recent_urls_set:
                recent_urls_set.add(link.url)
                ok_links.append(link)
        if len(recent_urls_set) == 8192:
            recent_urls_set.clear()
        return ok_links
