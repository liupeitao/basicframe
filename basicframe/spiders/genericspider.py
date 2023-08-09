import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import Rule, CrawlSpider
from scrapy.http import HtmlResponse

from basicframe.items.items import ArticleItem
from basicframe.midwares.redisclient import RedisClient
from basicframe.spiders.extractors.articelextractor import extractor_articel

from basicframe.playground.spot import judge_list, judge_list_by_html

url_set = set()


class GenericSpider(CrawlSpider):
    name = "generalspider"

    start_url = []
    # site_info = RedisClient.get_site_info_from_redis('多语种文本采集', name) or RedisClient.get_site_info_from_redis(
    #     '多语种文本采集', 'default')
    site_info = {'domains': '政治'}
    rules = (
        # Rule(LinkExtractor(restrict_xpaths=site_info.get('selector').get('page_xpath_restrict'),
        #                    allow=site_info.get('selector').get('page_allow'),
        #                    canonicalize=False),
        #      process_links='custom_process_links',
        #      follow=True),
        #
        # Rule(LinkExtractor(restrict_xpaths=site_info.get('selector').get('item_xpath_restrict'),
        #                    allow=site_info.get('selector').get('item_allow'),
        #                    ),
        #      callback='parse_item', follow=False, process_request='process_page_request'),
        Rule(LinkExtractor(allow=('page=', '&page', 'page/\\d+')),
             callback='parse_page', follow=True),

        Rule(LinkExtractor(),
             callback='parse_item', follow=False, process_links='custom_process_links'),
    )

    def start_requests(self):
        yield scrapy.Request(url=self.name)

    def process_page_request(self, request: scrapy.Request):
        request.priority = 2  # 越大月高
        return request

    def custom_process_links(self, links):
        ok_links = []
        for link in links:
            if link.url not in url_set:
                url_set.add(link.url)
                ok_links.append(link)
        if len(url_set) == 10000:
            url_set.clear()
        return ok_links

    def parse_item(self, response: HtmlResponse):
        if response.url.startswith(self.name):
            rs = judge_list_by_html(response.text)
            if rs > 0.9:
                return scrapy.Request(response.url)
            else:
                return None
        yield extractor_articel(response, self.site_info)

    def parse_page(self, response):
        pass

    def parse_all(self, response: HtmlResponse):
        pass
        # detail = 'xxxxxx'
        # if response.url is detail:
        #     pass
        #     # yield from self.parse_item(response)
        # else:
        #     yield self.parse_page(response)
