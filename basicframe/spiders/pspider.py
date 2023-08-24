import scrapy
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import Rule, CrawlSpider

from basicframe.spiders.extractors.articelextractor import extractor_articel

recent_urls_set = set()



# 适用于部分分页。会有一点误差。
class PenericSpider(CrawlSpider):
    rules = (
        Rule(LinkExtractor(allow='nba', canonicalize=True,deny='soccer'),
             follow=True,
             callback='parse_item',
             process_links='process_page_links',
    ),

    )

    def process_page_links(self, links):
        processd_links= self.not_recent_processed_links(links)
        return processd_links

    def start_requests(self):
        yield scrapy.Request(self.name)

    def process_page_request(self, request: scrapy.Request, response):
        return request

    def custom_process_links(self, links):
        processed_urls = self.not_recent_processed_links(links)
        return processed_urls

    def parse_item(self, response: HtmlResponse):
        articel_item = extractor_articel(response)
        articel_item.update(self.site_info)
        yield articel_item
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

