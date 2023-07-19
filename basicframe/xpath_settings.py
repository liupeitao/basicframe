XPATH_HASH_TABLE = {
    'site1': {
        'title': '//div[@class="title"]/h1/text()',
        'content': '//div[@class="content"]/p/text()',
        'pubTime': '//div[@class="meta"]/span[@class="pubTime"]/text()',
        'ctime': '//div[@class="meta"]/span[@class="ctime"]/text()',
        'lang': '//div[@class="meta"]/span[@class="lang"]/text()',
        'domain': '//div[@class="meta"]/span[@class="domain"]/text()',
        'subDomain': '//div[@class="meta"]/span[@class="subDomain"]/text()'
    },
    'site2': {
        'title': '//h1[@class="article-title"]/text()',
        'content': '//div[@class="article-content"]/p/text()',
        'pubTime': '//div[@class="article-meta"]/span[@class="pubTime"]/text()',
        'ctime': '//div[@class="article-meta"]/span[@class="ctime"]/text()',
        'lang': '//div[@class="article-meta"]/span[@class="lang"]/text()',
        'domain': '//div[@class="article-meta"]/span[@class="domain"]/text()',
        'subDomain': '//div[@class="article-meta"]/span[@class="subDomain"]/text()'
    }
}

XPATH_HASH_KEY = "article_xpath_setting"
