import json

import redis
import basicframe.settings as settings

POOL = redis.ConnectionPool.from_url(settings.REDIS_URL)


class RedisClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
            cls._instance.pool = redis.ConnectionPool.from_url(settings.REDIS_URL)
            cls._instance.redis_conn = redis.Redis(connection_pool=cls._instance.pool)
        return cls._instance

    def connect(self):
        return self.redis_conn

    @staticmethod
    def save_site_info_to_redis(name, domain,  **kwargs):
        r = RedisClient().connect()
        r.hset(name, domain, json.dumps(kwargs))

    @staticmethod
    def get_site_info_from_redis(name, domain) -> dict:
        r = RedisClient().connect()
        domain_info_dict = r.hget(name, domain)
        return json.loads(domain_info_dict.decode())


if __name__ == '__main__':
    domain_info = {
        'domains': '政治',
        'selector': {
            'type': 'Partial | Static',
            'item_allow': r'the-war-zone',
            'page_allow': r'page',
            'item_xpath_restrict': '//*[@id="incCont"]/div/article',
            'page_xpath_restrict': '//*[@id="pagCont"]/div/nav//@href'
        }
    }
    domain = 'https://www.thedrive.com/the-war-zone'
    name = '多语种文本采集'
    # RedisClient.save_site_info_to_redis("多语种文本采集", domain, **domain_info)
    # print(json.loads(RedisClient.get_site_info_from_redis(name, domain))
