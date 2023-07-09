from scrapy.linkextractors import LinkExtractor
from scrapy.utils.response import get_base_url
from scrapy.utils.python import unique as unique_list
from urllib.parse import urlparse
import redis
from scrapy.utils.project import get_project_settings

RDS = redis.StrictRedis(connection_pool=redis.ConnectionPool.from_url(get_project_settings()["REDIS_URL"]))

get_project_settings()["REDIS_URL"]


class ArticleLinkExtractor(LinkExtractor):

    def __init__(
            self,
            allow=(),
            deny=(),
            allow_domains=(),
            deny_domains=(),
            restrict_xpaths=(),
            tags=("a", "area"),
            attrs=("href",),
            canonicalize=False,
            unique=True,
            process_value=None,
            deny_extensions=None,
            restrict_css=(),
            strip=True,
            restrict_text=None,
            target=None

    ):
        super(ArticleLinkExtractor, self).__init__(allow, deny, allow_domains,
                                                   deny_domains, restrict_xpaths, tags,
                                                   attrs, canonicalize, unique,
                                                   process_value, deny_extensions,
                                                   restrict_css, strip, restrict_text
                                                   )
        self.target = target
        self.meta = {}

    def extract_links(self, response):
        if self.target:
            netloc = urlparse(response.url).netloc
            redis_key = "spider." + netloc

            xpath_selector = RDS.hget(redis_key, self.target)
            if xpath_selector:
                if isinstance(xpath_selector, bytes):
                    self.restrict_xpaths = xpath_selector.decode()
                else:
                    self.restrict_xpaths = xpath_selector

        base_url = get_base_url(response)
        if self.restrict_xpaths:
            docs = [
                subdoc for x in self.restrict_xpaths for subdoc in response.xpath(x)
            ]
        else:
            docs = [response.selector]
        all_links = []
        for doc in docs:
            links = self._extract_links(
                doc, response.url, response.encoding, base_url)
            all_links.extend(self._process_links(links))
        if self.link_extractor.unique:
            return unique_list(all_links)
        return all_links
