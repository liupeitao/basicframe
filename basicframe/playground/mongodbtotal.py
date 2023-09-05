from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://root:root123456@106.15.10.74:27017/admin')
db = client['mulwenben']

# Calculate total document count across all collections
total_docs = sum(db[collection].count_documents({}) for collection in db.list_collection_names())

print(f"Total number of documents across all collections: {total_docs}")
