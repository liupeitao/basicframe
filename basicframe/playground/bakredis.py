from basicframe.midwares.redisclient import RedisClient
redis_conn = RedisClient().connect()

urls = redis_conn.lrange('detailurls', 0, -1)
with open('tridetaibak11111.txt', mode='w') as f:
    for url in urls:
        c = url.decode()
        f.write(c+'\n')