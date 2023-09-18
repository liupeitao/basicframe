import re


def contains_substring(text, substr_tuple):
    for substr in substr_tuple:
        PAGE_PATTERN = re.compile(substr)
        if PAGE_PATTERN.search(text):
            return True
    return False

"""
Site type 1 部分静态
"""
# https://www.lavenir.net/regions/bruxelles/page-6/
# https://www.elespanol.com/elbernabeu/2418/

Partial_Static_Crawling = {
    'page_allow_tuple': (r'page=',
                         r'p=\d+',
                         r'&page',
                         r'page/\d+',
                         r'index\.\d+',
                         r'[\?&]page=\d+',
                         r'elder/\d+',
                         r'pno=\d+',
                         r'page-\d+',
                         r'/\d{1,5}/$',),
    'page_restrict_xpaths': '//*[not(self::header or ancestor::header or self::footer or ancestor::footer)]',
    'deny': ('view_type=',)
}

# {'start_url':'https://www.daily.co.jp/ring/'}

SITE_INFO_TABLE = {
    'https://www.thedrive.com/the-war-zone': {
        'domains': '政治',
        'selector': {
            'type': 'Partial | Static',
            'item_allow': r'the-war-zone',
            'page_allow': r'page',
            'item_xpath_restrict': '//*[@id="incCont"]/div/article',
            'page_xpath_restrict': '//*[@id="pagCont"]/div/nav'
        },
    },
    'https://www.cbsnews.com/politics/': {
        'domains': '政治',
        'selector': {
            'type': 'Partial | Static',
            'item_allow': r'/news/',
            'page_allow': 'politics',
            'item_xpath_restrict': '/html/body/div[6]/div/div[2]//a',
            'page_xpath_restrict': '//*[@id="component-topic-politics"]/div[2]'
        }
    },
    'default': {
        'domains': '政治',
        'selector': {
            'type': 'Partial | Static',
            'item_allow': [r'news', 'article', 'item'],
            'page_allow': ['page', r'/(\d+)/', 'next', 'late', 'before', r'index.\d+'],
            # 'item_xpath_restrict': ['//article', 'content', '//table'],
            # 'page_xpath_restrict': "//*[contains(text(), 'page') or contains(text(), 'next')]"
        }
    },
    'quanzhan': {
        'domains': '政治',
        'selector': {
            'type': 'Full | Static',
            'item_allow': '*',
            'page_allow': '*',
            # 'item_xpath_restrict': ['//article', 'content', '//table'],
            # 'page_xpath_restrict': "//*[contains(text(), 'page') or contains(text(), 'next')]"
        }
    }
}

XPATH_HASH_KEY = "setting"
