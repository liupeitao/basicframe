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
    def save_site_info_to_redis(name, domain, **kwargs):
        r = RedisClient().connect()
        r.hset(name, domain, json.dumps(kwargs))


    def rsave_site_info_to_redis(self, name, domain, **kwargs):
        self.connect().hset(name, domain, json.dumps(kwargs, ensure_ascii=False))

    @staticmethod
    def get_site_info_from_redis(name, domain) -> dict:
        r = RedisClient().connect()
        domain_info_dict = r.hget(name, domain) or {}
        if not domain_info_dict:
            return {}

        return dict(json.loads(domain_info_dict.decode()))


import pandas as pd





if __name__ == '__main__':
    pass
    # redis_conn RedisClient().connect()
