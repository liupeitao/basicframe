import math
import time

from gne import GeneralNewsExtractor
from goose3 import Goose
from scrapy.http import HtmlResponse

from basicframe.items.items import ArticleItem


def goose_extractor(html):
    article = Goose().extract(raw_html=html)
    return ArticleItem(title=article.title, content=article.cleaned_text, ctime=int(time.time()))


def gne_extractor(html):
    extractor = GeneralNewsExtractor()
    result = extractor.extract(html)
    return ArticleItem(title=result.get("title"), content=result.get("content"), ctime=int(time.time())
                       )


def extractor_articel(response: HtmlResponse, site_info: dict) -> ArticleItem:
    item = ArticleItem()
    item['url'] = response.url
    item["domain"] = site_info.get('domains')
    item['yield_time'] = math.ceil(time.time())
    for extractor in (goose_extractor, gne_extractor):
        ext = extractor(response.text)
        if ext["content"]:
            item["title"] = ext["title"]
            item["content"] = ext["content"]
            break
        else:
            continue
    return item
