import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import Rule, CrawlSpider
from scrapy.http import HtmlResponse

from basicframe.items.items import ArticleItem
from basicframe.midwares.redisclient import RedisClient
from basicframe.spiders.extractors.articelextractor import extractor_articel


class GenericSpider(CrawlSpider):
    name = "https://www.cbsnews.com/politics/"

    site_info = RedisClient.get_site_info_from_redis('多语种文本采集', name) or RedisClient.get_site_info_from_redis(
        '多语种文本采集', 'default')
    rules = (
        Rule(LinkExtractor(restrict_xpaths=site_info.get('selector').get('page_xpath_restrict'),
                           allow=site_info.get('selector').get('page_allow'),
                           canonicalize=False),
             process_links='custom_process_links',
             follow=True),

        Rule(LinkExtractor(restrict_xpaths=site_info.get('selector').get('item_xpath_restrict'),
                           allow=site_info.get('selector').get('item_allow'),
                           ),
             callback='parse_item', follow=False, process_request='process_page_request'),

    )

    def process_page_request(self, request: scrapy.Request):
        request.priority = 2  # 越大月高
        return request

    def custom_process_links(self, links):
        return links

    def start_requests(self):
        yield scrapy.Request(url=self.name)

    def parse_item(self, response) -> ArticleItem:
        item = extractor_articel(response, self.site_info)
        print(item)
        yield item

    def parse_page(self, response):
        return response

    def parse_all(self, response: HtmlResponse):
        detail = 'xxxxxx'
        if response.url is detail:
            yield self.parse_item(response)
        else:
            return self.parse_page(response)
