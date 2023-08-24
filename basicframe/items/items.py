# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BasicframeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ArticleItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    lang = scrapy.Field()
    domain = scrapy.Field()
    subDomain = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    ctime = scrapy.Field()
    pubTime = scrapy.Field()
    yield_time = scrapy.Field()
    sub_domain = scrapy.Field()