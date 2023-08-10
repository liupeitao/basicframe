import logging

import scrapy
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import Rule, CrawlSpider

from basicframe.test.logHandler import LogHandler
from basicframe.playground.spot import judge_list_by_html, judge_detail_by_html
from basicframe.spiders.extractors.articelextractor import extractor_articel

url_set = set()


class GenericSpider(CrawlSpider):
    name = ''
    # site_info = RedisClient.get_site_info_from_redis('多语种文本采集', name) or RedisClient.get_site_info_from_redis(
    #     '多语种文本采集', 'default')
    logger = LogHandler(name, file=True)
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
        yield scrapy.Request(self.name)

    def process_page_request(self, request: scrapy.Request):
        request.priority = 2  # 越大月高
        return request

    def custom_process_links(self, links):
        ok_links = []
        for link in links:
            if link.url not in url_set:
                url_set.add(link.url)
                ok_links.append(link)
        if len(url_set) == 8192:
            url_set.clear()
        return ok_links

    def parse_item(self, response: HtmlResponse):
        # 处理路径可能存在子路径
        if response.url.startswith(self.name):
            # 获取子路径的置信度
            rs = judge_list_by_html(response.text)
            if rs > 0.90:
                logging.info(f'{response.url} is sub_path of {self.name} probability: {rs}')
                return scrapy.Request(response.url)
            else:
                yield extractor_articel(response, self.site_info)
        else:
            rs = judge_detail_by_html(response.text)
            if rs > 0.35:
                yield extractor_articel(response, self.site_info)
            else:
                pass



    def parse_page(self, response):
        pass

    def parse_all(self, response: HtmlResponse):
        pass
