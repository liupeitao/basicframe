import scrapy
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import Rule, CrawlSpider

from basicframe.spiders.extractors.articelextractor import extractor_articel

recent_urls_set = set()
from basicframe.siteinfosettings import Partial_Static_Crawling as P_S_C


# 适用于部分分页。会有一点误差。
class GenericSpider(CrawlSpider):

    site_info = {'domains': '欧冠'}
    rules = (
        Rule(LinkExtractor(allow=P_S_C['page_allow_tuple'],
                           restrict_xpaths=P_S_C['page_restrict_xpaths'],
                           deny=P_S_C['deny'], canonicalize=True),
             follow=True,
             process_links='process_page_links',
             process_request='process_page_request'),

        Rule(LinkExtractor(canonicalize=True),
             callback='parse_item',
             follow=False,
             process_links='custom_process_links'),
    )

    def process_page_links(self, links):
        processed_urls = self.not_recent_processed_links(links)
        return processed_urls

    def start_requests(self):

        yield scrapy.Request(self.name)

    def process_page_request(self, request: scrapy.Request, response):
        self.spider_logger.info(f"processing page: {request.url}")
        request.meta['page_type'] = 'PAGE_TYPE'
        request.meta['max_retry_times'] = 3
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

