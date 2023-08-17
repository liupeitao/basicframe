import requests
import json


headers = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Origin": "https://www.politico.eu",
    "Pragma": "no-cache",
    "Referer": "https://www.politico.eu/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "content-type": "application/x-www-form-urlencoded",
    "sec-ch-ua": "\"Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"115\", \"Chromium\";v=\"115\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Linux\""
}
url = "https://a3cxkoqgf3-dsn.algolia.net/1/indexes/*/queries"
params = {
    "x-algolia-agent": "Algolia for JavaScript (4.17.1); Browser (lite); instantsearch.js (4.56.1); JS Helper (3.13.0)",
    "x-algolia-api-key": "138da0d7b154a5032735cfdcfda0e3cf",
    "x-algolia-application-id": "A3CXKOQGF3"
}
politico_file = open('../assets/2023_0815_待提交_politico_file.txt', mode='w')
page = 1
while True:
    data = {
        "requests": [
            {
                "indexName": "production_EU",
                "params": f"facets=%5B%22tagValues%22%5D&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&maxValuesPerFacet=10&page={page}&query=UEFA&tagFilters="
            }
        ]
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, params=params, data=data)
    hits = response.json()['results'][0]['hits']
    for hit in hits:
        print(hit['url'])
        politico_file.write(hit['url']+'\n')
    page+=1