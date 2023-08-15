import json

from basicframe.playground.tasks import news_processing_article

from pathlib2 import Path

src_file = Path('/home/liupeitao/c.txt')
res = open('../assets/celery_result1.txt', mode='w')
with src_file.open() as f:
    for line in f:
        line = line.strip()
        item = {
            'url': line,
            'domain': "政治"
        }
        # item = dict(json.loads(line))
        # item['url'] = item['url'].replace(' ', '')
        r = news_processing_article.delay(item)
        res.write(r.id+'\n')

