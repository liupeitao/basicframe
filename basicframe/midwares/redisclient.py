import redis

import basicframe.settings as settings


class RedisClient:
    _instance = None
    redis_url = 'redis://:Liupeitao1.@106.15.10.74:6379/0'

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host=None, port=None, db=None, password=None):
        self.host = host or settings.REDIS_HOST
        self.port = port or settings.REDIS_PORT
        self.db = db or settings.REDIS_DB
        self.password = password or settings.REDIS_PASSWORD
        self.__connection = None

    def connect(self):
        if not self.__connection:
            self.__connection = redis.Redis(host=self.host, port=self.port, db=self.db, password=self.password)
        return self.__connection


if __name__ == '__main__':
    redis_client = RedisClient()
    redis_conn = redis_client.connect()
