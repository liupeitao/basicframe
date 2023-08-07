
from scrapy.crawler import CrawlerProcess

from basicframe.spiders.genericspider import GenericSpider

# 实例化多个GenericSpider对象
spider1 = GenericSpider()
spider1.start_urls = ['https://www.thedrive.com/the-war-zone']

process = CrawlerProcess()
process.crawl(GenericSpider)
process.start()
