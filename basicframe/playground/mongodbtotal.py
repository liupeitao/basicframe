# import json
#
# from pymongo import MongoClient
# from pathlib2 import Path
# # Connect to MongoDB
# client = MongoClient('mongodb://root:root123456@106.15.10.74:27017/admin')
# db = client['mulwenben']
# count = 0
# dir = Path('/media/ptking/data/mulwenwen/0906')
# doc_set = set()
# # Calculate total document count across all collections
# for collection in db.list_collection_names():
#     if 'http' not in collection and 'sit' not in collection:
#         collection = collection.strip()
#         path = Path(dir/collection)
#         docs = db[collection].find({}, {'_id': 0})
#         try:
#             path.mkdir()
#         except Exception:
#             pass
#         for doc in docs:
#             if doc.get('domain'):
#                 domain_dir = Path(path/doc.get('domain'))
#                 if doc.get('sub_domain'):
#                     subdomain = Path(domain_dir/str(doc.get('sub_domain')))
#                 else:
#                     subdomain = Path(domain_dir/'no_sub_domain')
#             else:
#                 domain_dir = Path(path/'no_domain')
#                 subdomain = domain_dir
#             try:
#                 domain_dir.mkdir()
#                 subdomain.mkdir()
#             except Exception:
#                 pass
#             save_path = Path(subdomain/'articel').with_suffix('.json')
#             with open(save_path, mode='a') as f:
#                 f.write(json.dumps(doc, ensure_ascii=False) + '\n')
#                 print(count,  doc)
#                 count += 1
#
#
#
#
#
#
#
#
import json

# import json
#
from pymongo import MongoClient
from pathlib2 import Path
# Connect to MongoDB
client = MongoClient('mongodb://root:root123456@106.15.10.74:27017/admin')
db = client['mulwenben']
count = 0
dir = Path('/media/ptking/data/mulwenwen/0906')
# Calculate total document count across all collections
for collection in db.list_collection_names():
    collection = collection.strip()
    path = Path(dir / collection).with_suffix('.json')
    if Path.exists(path):
        continue
    if 'http' not in collection and 'sit' not in collection:
        docs = db[collection].find({}, {'_id': 0})
        with open(path, mode='a') as f:
            for doc in docs:
                f.write(json.dumps(doc) + '\n')
                print(count,  doc)
                count += 1