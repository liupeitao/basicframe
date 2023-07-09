import pymongo

from basicframe import settings

mongo_client = pymongo.MongoClient(settings.MONGO_URL)
dbName = settings.MONGO_DB
coll = settings.MONGO_COLL
# host = self.settings['MONGODB_HOST']
# port = self.settings['MONGODB_PORT']
# user = self.settings['MONGODB_USER']
# passwd = self.settings['MONGODB_PASSWD']
# client =pymongo.MongoClient(host=host, port=port,
#                            username=user, password=passwd, authSource="admin")
