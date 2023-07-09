import time

from gne import GeneralNewsExtractor
from goose3 import Goose
from scrapy.http import HtmlResponse
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider

from basicframe.items.articleitems import ArticleItem
from basicframe.spiders.extractors.link_extractor import ArticleLinkExtractor


class ArticleSpider(RedisCrawlSpider):
    name = 'ArticleSpider'
    redis_key = "article_spider:start_urls"
    max_idle_time = 7111
    # allowed_domains = ["www.liaoxuefeng.com"]
    # start_urls = ['https://www.lemonde.fr/musiques/']

    article_xpath_extractor = ArticleLinkExtractor(deny=["/search", "/auth", "#", "sign", "login", "redirect"],
                                                   canonicalize=False,
                                                   restrict_xpaths="//*[contains(@class,'post') or contains(@class,'cate') or contains(@class,'article') or contains(@class,'cont' )]|//article",
                                                   target="link")
    article_link_extractor = ArticleLinkExtractor(
        allow="(article|post|content)", canonicalize=False, )

    rules = (
        Rule(link_extractor=article_xpath_extractor,
             callback='parse_item'),
        Rule(link_extractor=article_link_extractor,
             callback='parse_item'),
        Rule(ArticleLinkExtractor(allow="/page", target="page", canonicalize=False),
             callback='parse_page', follow=True),
    )

    def my_request_processor(self, request, response):
        request.meta["domain"] = response.meta["domain"]
        request.meta["subDomain"] = response.meta["subDomain"]
        request.meta["lang"] = response.meta["lang"]
        return request

    def parse_page(self, response: HtmlResponse):
        print(response.url, "============")

    def parse_item(self, response):

        yield self.iter_extractor(response)

    def goose_extractor(self, html):
        article = Goose().extract(raw_html=html)
        return ArticleItem(title=article.title, content=article.cleaned_text, ctime=int(time.time()))

    def gne_extractor(self, html):
        extractor = GeneralNewsExtractor()
        result = extractor.extract(html)
        return ArticleItem(title=result.get("title"), content=result.get("content"), ctime=int(time.time())
                           )

    def iter_extractor(self, response: HtmlResponse):
        item = ArticleItem()
        item["domain"] = response.meta.get("domain")
        item["subDomain"] = response.meta.get("subDomain")
        item["lang"] = response.meta.get("lang")
        for extractor in (self.gne_extractor, self.goose_extractor):
            ext = extractor(response.text)
            if ext["content"]:
                item["title"] = ext["title"]
                item["content"] = ext["content"]
                return item
            else:
                continue
        item["content"] = "".join(response.xpath("//body//text()").extract())

        print(item)
        return item
