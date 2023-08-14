def generate_std_name(url):
    return f"{url.replace('/', '_').replace(':', '_').replace('.', '_')}"
