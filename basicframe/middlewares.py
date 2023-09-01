# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random

import requests
import scrapy.http
from fake_useragent import UserAgent
from scrapy import signals
from twisted.internet.error import TCPTimedOutError

from basicframe.utils.logHandler import LogHandler


# useful for handling different item types with a single interface


class BasicframeSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class BasicframeDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class ProxyMiddleware(object):
    def __init__(self):
        self.counter = 1
        self.proxys = None
        self.bad_response_code = set(range(400, 600)).union(range(100, 200))
        self.vpn_proxy = "http://127.0.0.1:7890"
        self.proxy = None
        self.change_proxy_times = 0
        self.chage_vpn_proxy_times = 0
    def update_proxy_pool(self, logger: LogHandler):
        try:
            ip_port_list = requests.get("https://servers.qunyindata.com/GetWDProxy?count=50").json()["results"]
            self.proxys = [f'http://{ip_port}' for ip_port in ip_port_list]
        except Exception as e:
            logger.warning(f'get random proxy faild, use default vpn_proxy {self.vpn_proxy}')
            self.proxys = [self.vpn_proxy]

    def get_one_proxy(self, logger: LogHandler):
        if not self.proxys or self.counter % 100 == 0:
            self.update_proxy_pool(logger)
        return random.choice(self.proxys)

    def process_request(self, request: scrapy.http.Request, spider):
        # self.change_proxy_times += 1
        headers = {
            "User-Agent": UserAgent().random
        }
        request.headers.update(headers)
        # request.meta['proxy'] = None
        print(request.headers['User-Agent'])
        # print(f"TestProxyMiddleware --> {request.meta['proxy']}")

    # def process_response(self, request: scrapy.http.Request, response, spider):
    #     logger = spider.spider_logger
    #     if response.status in self.bad_response_code:
    #         new_proxy = self.get_one_proxy(spider.spider_logger)
    #         request.meta['proxy'] = new_proxy
    #         logger.error(f'{response.status} using new proxy in proxypool {new_proxy} <self.proxy: {self.proxy}> {request.url}')
    #         return request.replace(dont_filter=True)
    #     else:
    #         return response

    # def process_exception(self, request: scrapy.http.Request, exception, spider):
    #     if isinstance(exception, (TimeoutError, ConnectionError, TCPTimedOutError)):
    #         spider.spider_logger.error("TimeoutError encountered, switching proxy...")
    #
    #     new_proxy = self.vpn_proxy
    #     self.chage_vpn_proxy_times += 1
    #     if self.chage_vpn_proxy_times > 10:
    #         self.proxy = self.vpn_proxy
    #         return request.replace(dont_filter=True)
    #     elif new_proxy:
    #         spider.spider_logger.info(f"using new proxy(vpn): {new_proxy} <self.proxy: {self.proxy}> {request.url}")
    #         # 为请求设置新的代理，并重新调度
    #         request.meta['proxy'] = new_proxy
    #         return request.replace(dont_filter=True)
    #     else:
    #         return None  # 继续处理该异常

