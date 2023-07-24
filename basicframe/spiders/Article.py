import time
import urllib

import scrapy
from gne import GeneralNewsExtractor
from goose3 import Goose
from scrapy.exceptions import IgnoreRequest
from scrapy.http import HtmlResponse
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider

from basicframe.filters.filter import FilterChain, NetFilter
from basicframe.items.articleitems import ArticleItem
from basicframe.spiders.extractors.link_extractor import ArticleLinkExtractor


class ArticleSpider(RedisCrawlSpider):
    name = 'ArticleSpider'
    redis_key = "article_spider:start_urls"
    max_idle_time = 7111
    # allowed_domains = ["www.liaoxuefeng.com"]
    # start_urls = ['https://www.lemonde.fr/musiques/']

    article_xpath_extractor = ArticleLinkExtractor(deny=["/search", "/auth", "#", "sign", "login", "redirect"], canonicalize=False,
                                                   restrict_xpaths="//*[contains(@class,'post') or contains(@class,'cate') or contains(@class,'article') or contains(@class,'cont' )]|//article", target="link")
    article_link_extractor = ArticleLinkExtractor(
        allow="(article|post|content)", canonicalize=False,)

    rules = (
        Rule(link_extractor=article_xpath_extractor,
             callback='parse_item',
             process_request='process_request_callback'
             ),
        Rule(link_extractor=article_link_extractor,
             callback='parse_item',
             process_request='process_request_callback'
             ),
        Rule(ArticleLinkExtractor(allow="/page", target="page", canonicalize=False),
             callback='parse_page', follow=True,
             process_request='process_request_callback'
             ),
    )

    def process_request_callback(self, request: scrapy.Request, response):
        filter_chain = FilterChain()
        xinyuan_filter = NetFilter()
        filter_chain.add_filter(xinyuan_filter)
        if filter_chain.do_filter(request.url, '2'):
            print(f"{request.url} 是否可以通过:True: 转交后续处理")
            xinyuan_meta = xinyuan_filter.get_xinyuan_meta()
            request.meta['domain'] = xinyuan_meta[urllib.parse.urlparse(request.url).netloc]['domain']
            return request
        else:
            print(f"{request.url} 是否可以通过:False， 将被丢弃")
            IgnoreRequest(request)

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
        item['url'] = response.url
        item["domain"] = response.meta.get("domain")
        # item["subDomain"] = response.meta.get("subDomain")
        # item["lang"] = response.meta.get("lang")
        for extractor in (self.gne_extractor, self.goose_extractor):
            ext = extractor(response.text)
            if ext["content"]:
                item["title"] = ext["title"]
                item["content"] = ext["content"]
                return item
            else:
                continue
        item["content"] = ""
        return item
