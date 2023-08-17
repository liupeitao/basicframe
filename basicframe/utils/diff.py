import json
from difflib import SequenceMatcher

from basicframe.utils.peekurl import get_urls_from_page


def likely_url_groups(url_list, threshold) -> dict:
    link_groups = {}  # 链接组字典
    for link in url_list:
        added_to_group = False
        for group_link in link_groups.keys():
            similarity = SequenceMatcher(None, link, group_link).ratio()
            if similarity >= threshold:
                link_groups[group_link].append(link)
                added_to_group = True
                break
        if not added_to_group:
            link_groups[link] = [link]
    return link_groups


def process_one_url(url, f, threshold=0.90):
    url_list = get_urls_from_page(url)
    if not url_list:
        f.write(url)
        return
    url_list = list(set(url_list))

    # threshold阈值，用于确定链接的相似度阈值
    link_groups = likely_url_groups(url_list, threshold)
    f.write(json.dumps(link_groups))


def print_url_info(link_groups: dict):
    for group, group_links in link_groups.items():
        if len(group_links) > 1:
            print("group:")
            for link in group_links:
                print(link)
