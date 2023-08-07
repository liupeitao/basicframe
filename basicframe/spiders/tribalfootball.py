import scrapy
from gne import GeneralNewsExtractor
from goose3 import Goose
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from basicframe.items.items import ArticleItem


class TribalfootballSpider(CrawlSpider):
    name = "tribalfootball"
    allowed_domains = ["www.tribalfootball.com"]
    def start_requests(self):
        with open('basicframe/b.txt', mode='r') as f:
            for url in f:
                url = url.strip()
                yield scrapy.Request(url=url)

    custom_settings = {
        "MONGO_COLL": name
    }
    rules = (Rule(LinkExtractor(allow=r"articles", restrict_xpaths="//div[@class='pagination']/preceding-sibling::div[1]//a"), callback="parse_item"),
             Rule(LinkExtractor(allow='page', restrict_xpaths='/html/body//ul[contains(@class, "pagination__pages")]'), follow=True, callback='parse_page', process_links='custom_process_links')
             # Rule(LinkExtractor(allow='page', restrict_css='ul.pagination__pages li a[href*=\\d]'))
             )
    def parse_page(self, response):
        pass

    def custom_process_links(self, links):
        print(links)
        return links

    def goose_extractor(self, html):
        article = Goose().extract(raw_html=html)
        return ArticleItem(
            title=article.title, content=article.cleaned_text,
            pubTime=article.publish_date
        )

    def gne_extractor(self, html):
        extractor = GeneralNewsExtractor()
        result = extractor.extract(html)
        return ArticleItem(
            title=result.get("title"), content=result.get("content"),
            pubTime=result.get("publish_time")
        )

    def parse_item(self, response: HtmlResponse):
        item = ArticleItem()
        item["url"] = response.url
        item["domain"] = "欧冠"  # "#response.meta['domain']
        for extractor in (self.goose_extractor, self.gne_extractor):
            ext = extractor(response.text)
            if ext["content"]:
                item["title"] = ext["title"]
                item["content"] = ext["content"]
                item["pubTime"] = ext["pubTime"]
                break
            else:
                item["content"] = ""
                continue
        yield item