import json
from pymongo import MongoClient


def insert_to_mongodb(file_path, db_name, mongo_url, coll_name):
    client = MongoClient(mongo_url)
    db = client[db_name]
    collection = db[coll_name]

    documents = []
    with open(file_path, 'r') as file:
        for line in file:
            try:
                document = json.loads(line.strip())
                documents.append(document)
            except json.JSONDecodeError as e:
                print("Error decoding JSON:", e)
                continue

    if documents:
        try:
            result = collection.insert_many(documents)
            print("Inserted documents:", result.inserted_ids)
        except Exception as e:
            print("Error inserting documents:", e)

    client.close()


input_file_path = 'duoyuzhong11.txt'
db_name = 'mulwenben'
mongo_url = 'mongodb://root:root123456@106.15.10.74:27017/admin'
coll_name = 'siteinfo'

insert_to_mongodb(input_file_path, db_name, mongo_url, coll_name)
