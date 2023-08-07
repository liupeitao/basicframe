from scrapy import Request
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import Rule, CrawlSpider

from basicframe.midwares.redisclient import RedisClient
from basicframe.spiders.extractors.articelextractor import extractor_articel


class GenericSpider(CrawlSpider):
    name = "https://www.thedrive.com/the-war-zone"
    site_info = RedisClient.get_site_info_from_redis('多语种文本采集', name)

    rules = (
        Rule(link_extractor=LinkExtractor(restrict_xpaths=site_info.get('selector').get('item_xpath_restrict'),
                                          allow=site_info.get('selector').get('item_allow'),
                                          ),
             callback='parse_item',
             ),

        Rule(link_extractor=LinkExtractor(restrict_xpaths=site_info.get('selector').get('page_xpath_restrict'),
                                          allow=site_info.get('selector').get('page_allow'),
                                          canonicalize=False),
             follow=True),
    )

    def start_requests(self):
        yield Request(url=self.name)

    def parse_item(self, response):
        item = extractor_articel(response, self.site_info)
        yield item
