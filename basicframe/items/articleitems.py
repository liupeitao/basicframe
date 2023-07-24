# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
class ArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # lang = scrapy.Field()
    domain = scrapy.Field()
    # subDomain = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    ctime = scrapy.Field()
    pubTime = scrapy.Field()
    url = scrapy.Field()
