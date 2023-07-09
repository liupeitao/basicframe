import requests
from basicframe.utils.decorator import request_with_progress


@request_with_progress
def make_request(url):
    return requests.get(url, stream=True)