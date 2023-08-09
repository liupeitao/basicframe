import subprocess


def get_url_list(start_url):
    ret = subprocess.run(
        args=['urlfinder', '-x', 'http://127.0.0.1:7890', '-u', start_url],
        stdout=subprocess.PIPE)
    try:
        res = ret.stdout.decode('utf-8')
    except UnicodeDecodeError as e:
        print(e.start)
        print(e)
        print("error url", start_url)
        return []
    try:
        res = res.split('URL to')[1]
        url_list = []
        for url in res.split('\n'):
            url_list.append(url)
        return list(set(url_list))
    except IndexError as e:
        return []