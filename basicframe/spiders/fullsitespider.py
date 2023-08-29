import scrapy
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider

from basicframe.spiders.genericspider import extractor_articel

recent_urls_set = set()


class FullSiteSpider(RedisCrawlSpider):
    def start_requests(self):
        yield scrapy.Request(url=self.name)

    custom_settings = {
        'RETRY_ENABLED': False,
        # 爬虫空闲时从 redis 取数据频率
        # 'SCHEDULER_IDLE_BEFORE_CLOSE': 1300,
        # 一次从 redis 中拿取最大量
        'CONCURRENT_REQUESTS': 32,
        # 一个域名下最大的并发数（测试-历史数据）
        'CONCURRENT_REQUESTS_PER_DOMAIN': 64,

        # 是否禁用cookie
        # 'REQUESTS_DISABLE_COOKIES': False,

        # 是否禁用重定向
        'REQUESTS_FOLLOW_REDIRECTS': False,

        # 全站使用布隆过滤器
        # 'SCHEDULER': "scrapy_redis_bloomfilter.scheduler.Scheduler",
        # 'DUPEFILTER_CLASS': "scrapy_redis_bloomfilter.dupefilter.RFPDupeFilter",
        # 'BLOOMFILTER_HASH_NUMBER': 6,
        # 'BLOOMFILTER_BIT': 30,
        # 'SCHEDULER_PERSIST': True
    }
    rules = (
        Rule(
            LinkExtractor(
                deny=[
                    "/search", "/auth", "sign", "login",
                    '.*jpg', '.*jpeg', '.*mp4', '.*gif', '.*png', '.*pdf',
                    '.*doc', '.*docx', "javascript",
                    "/image", "/img", "/pic", 'video'
                ],
                canonicalize=True
            ),
            follow=True,
            callback='parse_item',
            process_request='process_request_callback',
            process_links='process_links_callback',
        ),
    )

    def process_request_callback(self, request: scrapy.Request, response):
        self.spider_logger.info(f'{request.url}')
        return request

    def process_links_callback(self, links):
        processed_links = self.not_recent_processed_links(links)
        return processed_links

    def parse_item(self, response: HtmlResponse):
        site_info = {'domain': 'ouguan'}
        item = extractor_articel(response)
        item.update(site_info)
        yield item

    @staticmethod
    def not_recent_processed_links(links):
        ok_links = []
        for link in links:
            if link.url not in recent_urls_set:
                recent_urls_set.add(link.url)
                ok_links.append(link)
        if len(recent_urls_set) == 20480:
            recent_urls_set.clear()
        return ok_links
