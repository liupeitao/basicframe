import json

from basicframe.playground.tasks import news_processing_article

from pathlib2 import Path

src_file = Path('../assets/2023_0815_待提交_politico_file.txt')
res = open('../2023_0815_待提交_politico_file.json', mode='w')
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

