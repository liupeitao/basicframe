from scrapy import cmdline


def execute_spider(spider_name):
    cmdline.execute(f"scrapy crawl {spider_name}".split())


def main(spider_name):
    execute_spider(spider_name)


if __name__ == '__main__':
    main()
