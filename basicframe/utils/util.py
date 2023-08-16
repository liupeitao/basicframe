from datetime import datetime

proxies = {
    'http': 'http://localhost:7890',
    'https': 'https://localhost:7890',
}


def generate_std_name(url):
    return f"{url.replace('/', '_').replace(':', '_').replace('.', '_')}"


def current_date_time(strf="%Y_%m_%d_%H:%M"):
    now = datetime.now()
    time_str = now.strftime(strf)
    return time_str
