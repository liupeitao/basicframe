from pymongo import MongoClient
import basicframe.settings as settings


class MongoDBClient:
    _instance = None
    mongo_url = settings.MONGO_URL

    def __init__(self, host=None, port=None):
        self.host = host or settings.MONGODB_HOST
        self.port = port or settings.MONGODB_PORT

    def connect(self):
        return MongoClient(self.host, self.port)


mongo_client = MongoDBClient().connect()
