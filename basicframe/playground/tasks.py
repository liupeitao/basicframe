import json
import time

import requests
from celery import Celery
from goose3 import Goose
from newspaper import Article
from basicframe.midwares.celeryclient import app
from basicframe.midwares.mongodbclient import MongoDBClient
from basicframe.spiders.extractors.articelextractor import extractor_articel_gen
mongo = MongoDBClient().connect()['article']['0814cnn']

@app.task(queue='news_processing_queue')
def news_processing_article(news_info):
    site_info = {
        'domains': news_info['domain']
    }
    response = requests.get(news_info['url'])
    news_data = extractor_articel_gen(response, site_info)
    if len(news_data['content']) > 200:
        mongo.insert_one(dict(news_data))
        print(news_data)
    return news_data