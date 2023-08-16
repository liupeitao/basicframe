import re
from basicframe.siteinfosettings import Partial_Static_Crawling as P_S_C
page_allow_tuple = P_S_C['page_allow_tuple']
def test_page_allow_tuple():
    url1 = 'https://terms.naver.com/list.naver?cid=41701&categoryId=41701&so=st3.asc&viewType=&categoryType=&index=0-9#content'
    flag = False
    for index, pattern in enumerate(page_allow_tuple):
        PATTERN = re.compile(pattern)
        match = PATTERN.search(url1)
        if match:
            print(f"匹配第{index+1}个正则:{pattern}")
            flag = True
            break
    assert flag, "No pattern from page_substr_tuple found in the URL."