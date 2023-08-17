import requests

from basicframe import settings
from basicframe.midwares.celeryclient import app
from basicframe.midwares.dbclient import DbClient
from basicframe.spiders.extractors.articelextractor import extractor_articel_gen

mongo_client = DbClient(settings["MONGO_URL"])
mongo_client.change_table('')


@app.task(queue='news_processing_queue')
def news_processing_article(news_info):
    site_info = {
        'domains': news_info['domain']
    }
    response = requests.get(news_info['url'])
    news_data = extractor_articel_gen(response, site_info)
    if len(news_data['content']) > 200:
        mongo_client.put(dict(news_data))
        print(news_data)
    return news_data
