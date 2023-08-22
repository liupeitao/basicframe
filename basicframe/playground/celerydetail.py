import json

from basicframe.playground.tasks import news_processing_article, tripagetodetail,  news_processing_article


from basicframe.midwares.redisclient import RedisClient
redis_conn = RedisClient().connect()


def run_tasks_from_redis():
    for i in range(50000):
        # This will block until an item is available
        _, url = redis_conn.brpop('detailurls',10)

        news_info = {'url': url.decode('utf-8')}
        x = news_processing_article.delay(news_info)
        print(x)

if __name__ == '__main__':
    run_tasks_from_redis()
