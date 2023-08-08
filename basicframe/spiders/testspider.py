# import scrapy
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders.crawl import Rule, CrawlSpider
#
# from basicframe.midwares.redisclient import RedisClient
# from basicframe.spiders.extractors.articelextractor import extractor_articel
#
#
# class GenericSpider(CrawlSpider):
#     name = "https://www.thedrive.com/the-war-zone"
#     max_url_len = ''
#     site_info = {'domains': '1'}
#     rules = (
#         Rule(LinkExtractor(),
#              process_links='custom_process_links',
#              follow=True),
#     )
#     def process_page_request(self, request: scrapy.Request):
#         if request.url
#         request.priority = 2  # 越大月高
#         return request
#
#     def custom_process_links(self, links):
#
#         return links
#
#     def start_requests(self):
#         yield scrapy.Request(url=self.name)
#
#     def parse_item(self, response):
#         item = extractor_articel(response, self.site_info)
#         print(item)
#
