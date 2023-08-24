import math
import time

from gne import GeneralNewsExtractor
from goose3 import Goose
from newspaper import Article
from scrapy.http import HtmlResponse

from basicframe.items.items import ArticleItem


def goose_extractor(html):
    article = Goose().extract(raw_html=html)
    return ArticleItem(title=article.title, content=article.cleaned_text)


def gne_extractor(html):
    extractor = GeneralNewsExtractor()
    result = extractor.extract(html)
    return ArticleItem(title=result.get("title"), content=result.get("content")
                       )

def newspaper_extractor(html):
    article = Article(url="")  # URL和语言可根据实际情况修改
    article.set_html(html)
    article.parse()
    return ArticleItem(title=article.title, content=article.text)

def extractor_articel_gen(response, site_info: dict) -> dict:
    item = {'url': response.url, "domain": site_info.get('domains'), 'yield_time': math.ceil(time.time())}
    for extractor in (gne_extractor, goose_extractor):
        try:
            ext = extractor(response.text)
            item["title"] = ext["title"]
            item["content"] = ext["content"]
            return item
        except Exception as e:
            continue
    return item


def extractor_articel(response: HtmlResponse) -> ArticleItem:
    item = ArticleItem()
    item['url'] = response.url
    item['yield_time'] = math.ceil(time.time())
    for extractor in (newspaper_extractor, gne_extractor, goose_extractor):
        try:
            ext = extractor(response.text)
            item["title"] = ext["title"]
            item["content"] = ext["content"]
            return item
        except Exception as e:
            continue
    return item
