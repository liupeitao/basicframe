import json

from pymongo import MongoClient
from pathlib2 import Path
# Connect to MongoDB
client = MongoClient('mongodb://root:root123456@106.15.10.74:27017/admin')
db = client['mulwenben']
count = 0
dir = Path('/media/ptking/data/mulwenwen/0906')
doc_set = set()
# Calculate total document count across all collections
for collection in db.list_collection_names():
    if 'http' not in collection and 'sit' not in collection:
        collection = collection.strip()
        path =Path(dir/collection)
        path.mkdir(exist_ok=True)
        docs = db[collection].find({}, {'_id': 0})
        for doc in docs:
            if doc.get('领域'):
                domain_dir = Path(path/doc.get('领域'))
                if doc.get('子领域'):
                    subdomain = Path(domain_dir/doc.get('子领域'))
                else:
                    subdomain = Path(domain_dir/'no_sub_domain')
            else:
                domain_dir = Path(path/'no_domain')
                subdomain = domain_dir
            domain_dir.mkdir(exist_ok=True)
            subdomain.mkdir(exist_ok=True)
            save_path = Path(subdomain/'articel').with_suffix('.json')
            with open(save_path, mode='w') as f:
                f.write(json.dumps(doc) + '\n')
                print(count,  doc)
                count += 1








