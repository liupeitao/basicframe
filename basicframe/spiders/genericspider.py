import scrapy
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import Rule, CrawlSpider
from scrapy_redis.spiders import RedisCrawlSpider

from basicframe.spiders.extractors.articelextractor import extractor_articel

from basicframe.siteinfosettings import Partial_Static_Crawling as P_S_C


# 适用于部分分页。会有一点误差。
class GenericSpider(RedisCrawlSpider):
    recent_urls_set = set()
    rules = (
        Rule(LinkExtractor(allow=P_S_C['page_allow_tuple'],
                           restrict_xpaths=P_S_C['page_restrict_xpaths'],
                           deny=P_S_C['deny'], canonicalize=True),
             callback='parse_item',
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
        self.spider_logger.info(f"spider start!!!: {self.name} spider type: {self.type} {self.site_info}")
        yield scrapy.Request(self.name)

    def process_page_request(self, request: scrapy.Request, response):
        self.spider_logger.info(f"processing page: {request.url}")
        request.meta['max_retry_times'] = 3
        return request

    def custom_process_links(self, links):
        processed_urls = self.not_recent_processed_links(links)
        return processed_urls

    def parse_item(self, response: HtmlResponse):
        self.spider_logger.info(f"processing detail: {response.url}")
        article_item = extractor_articel(response)
        article_item.update(self.site_info)
        yield article_item

    def not_recent_processed_links(self, links):
        processed_urls = []
        for link in links:
            if link.url not in self.recent_urls_set:
                self.recent_urls_set.add(link.url)
                processed_urls.append(link)
        if len(self.recent_urls_set) == 10240:
            self.recent_urls_set.clear()
        self.spider_logger.debug(
            f"processed_urls:{[link.url for link in processed_urls]}, remove:{len(links) - len(processed_urls)} links!!")
        return processed_urls
