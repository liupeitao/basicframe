import requests
from lxml import html

# 假设你已经有一个包含所有页面URL的列表，命名为urls
urls = [
    "https://www.tribalfootball.com/leagues/english-premier-league?page=1",
    "https://www.tribalfootball.com/leagues/english-premier-league?page=2",
    # 其他页面URL
]

base_url = "https://www.tribalfootball.com"

detail_urls = []

for url in urls:
    response = requests.get(url)
    content = response.content
    tree = html.fromstring(content)

    # 使用lxml解析HTML获取详情页URL
    urls = tree.xpath('//*[@class="grid__item palm-one-half desk-wide-one-third"]//a/@href')
    # 拼接完整URL
    detail_urls.extend([base_url + url for url in urls])

print(detail_urls)