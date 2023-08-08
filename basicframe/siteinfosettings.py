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
            'page_allow': ['page', r'/(\d+)/', 'next', 'late', 'before'],
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
