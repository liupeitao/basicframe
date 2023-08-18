import pymongo
import scrapy
from redis.client import Redis
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
import re
from article_spider.articelextractor import parse_articel
from urllib.parse import urljoin
redis_client = Redis.from_url("redis://:qunyin@123@101.35.228.6:6379/3")
# pa = re.compile('href="(\?page=\d+)" class="pagination__btn pagination__btn--older pagination__btn--active">Older')
pa = re.compile('<li><a href="\?page=\d+">(\d+)</a></li>')
trew = open('trisfwe08171.txt', mode='a')
class FootboallSpider6(RedisCrawlSpider):
    name = "tribalfootballw"
    allowed_domains = ["www.tribalfootball.com"]
    total = 0
    def start_requests(self):
        for i in range(500):
            # url = redis_client.rpop('triboall')
            url = redis_client.lpop('triboall_bak')
            url = url.decode()
            redis_client.lpush('triboall_bak', url)
            yield scrapy.Request(url, callback=self.parse_category)

    # rules = {
    #     Rule(link_extractor=LinkExtractor(allow='/leagues/', restrict_xpaths='/html/body/div[2]/div[3]'), callback="parse_category", follow=False),
    # }
    # def pares(self, response):
    #     print(response.url)

    # def parse_category(self, response):
    #     yield scrapy.Request(url=urljoin(response.url, '?page=300000'), callback=self.parse_last)

    # def parse_last(self, response):
    #     str = response.css('div .pagination > ul > li')[-1].get()
    #     page_url = int(pa.findall(str)[0])
    #     self.total += page_url
    #     print(self.total)
    #     print(page_url)
        # for i in range(1, page_url+1):
        #     x = urljoin(response.url, f"?page={i}")
        #     print(x)
            # redis_client.lpush('triboall', x)


    def parse_category(self, response: scrapy.http.HtmlResponse):
        if response.status != 200:
            redis_client.lpush('tri_errors')
        part_url = response.css('div .grid__item.palm-one-half.desk-wide-one-third > a::attr(href)').getall()
        urls = []
        for s in part_url:
            url = urljoin('https://www.tribalfootball.com/leagues', s)
            urls.append(url)
            trew.write(url+'\n')
            redis_client.lpush('tridetail', url)



    # def custom_process_category(self, links, response):
    #     Rule(LinkExtractor(allow=(r'leagues')),
    #          callback="parse_item",
    #          follow=True,
    #          process_links='custom_process_links',
    #          process_request='custom_process_request'),
    #
    #
    # def parse_item(self, response):
    #     articel_item = parse_articel(response)
    #     yield articel_item
