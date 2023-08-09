import subprocess


def get_url_list(start_url):
    ret = subprocess.run(
        args=['urlfinder', '-u', start_url],
        stdout=subprocess.PIPE)
    res = ret.stdout.decode('utf-8')
    try :
        res = res.split('URL to')[1]
        url_list = []
        for url in res.split('\n'):
            url_list.append(url)
        return url_list
    except IndexError as e:
        return []