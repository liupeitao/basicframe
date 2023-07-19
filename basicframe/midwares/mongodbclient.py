from pymongo import MongoClient
import basicframe.settings as settings

class MongoDBClient:
    _instance = None
    mongo_url = settings.MONGO_URL

    def connect(self):
        return MongoClient(self.mongo_url)

mongo_client = MongoDBClient().connect()