import os
from scrapy import cmdline

def execute_spider(spider_name):
    cmdline.execute(f"scrapy crawl {spider_name}".split())

def main():
    spider_names = ['ArticleSpider']
    for spider_name in spider_names:
        execute_spider(spider_name)


if __name__ == '__main__':
   main()

