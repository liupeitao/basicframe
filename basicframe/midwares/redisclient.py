import redis
import basicframe.settings as settings
from basicframe.utils.log import get_logger
POOL = redis.ConnectionPool.from_url(settings.REDIS_URL)


class RedisClient:
    def __init__(self, host=None, port=None, db=None, password=None):
        self.host = host
        self.port = port
        self.db = db
        self.password = password

    def connect(self):
        return redis.Redis(connection_pool=POOL) or redis.from_url(settings.REDIS_URL)

