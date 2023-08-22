import re
from urllib.parse import urljoin

import scrapy
from redis.client import Redis
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
redis_client = Redis.from_url("redis://:qunyin@123@101.35.228.6:6379/3")
pa = re.compile('<li><a href="\?page=\d+">(\d+)</a></li>')

class TrixSpider(CrawlSpider):
    name = "trix"
    # allowed_domains = ["www.tribalfootball.com"]
    start_urls = ["https://www.tribalfootball.com/leagues"]
    rules = {
        Rule(link_extractor=LinkExtractor(allow='/leagues/', restrict_xpaths='/html/body/div[2]/div[3]'), callback="parse_category", follow=False),
    }
    total = 0
    def parse_category(self, response):
        yield scrapy.Request(url=urljoin(response.url, '?page=300000'), callback=self.parse_last)

    def parse_last(self, response):
        str = response.css('div .pagination > ul > li')[-1].get()
        file1 = open('assets/trix.txt', mode='a')
        page_url = int(pa.findall(str)[0])
        # print(self.total)
        print(response.url, page_url)

        file1.write(f"{response.url} {page_url }\n")
        for i in range(1, page_url + 1):
            x = urljoin(response.url, f"?page={i}")
            # print(x)
            # redis_client.lpush('tripage', x)
        print(self.total)