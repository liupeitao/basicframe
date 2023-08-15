
proxy_info = {
    'http': 'http://localhost:7890',
    'https': 'https://localhost:7890',
}
def generate_std_name(url):
    return f"{url.replace('/', '_').replace(':', '_').replace('.', '_')}"
