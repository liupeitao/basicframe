import requests

from basicframe.spiders.extractors.articelextractor import extractor_articel_gen
def test_extractor_articel():
    response = requests.get('https://terms.naver.com/list.naver?cid=44506&categoryId=64576')
    site_info = {'domains': 'fwe'}
    print(extractor_articel_gen(response, site_info))
