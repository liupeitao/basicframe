import json

from pathlib2 import Path

def replace_newlines(s):
    return s.replace('\n\n', '\r\n')

def process_per_line(doc, path: Path):
    doc['content'] = replace_newlines(doc['content'])
    if str(doc.get('domain')) and str(doc.get('domain')) != 'nan' and str(doc.get('domain')) != '/':
        domain_dir = Path(path / doc.get('domain'))
        if str(doc.get('sub_domain')) and str(doc.get('sub_domain')) != 'nan' and str(doc.get('sub_domain')) != '/':
            subdomain = Path(domain_dir/str(doc.get('sub_domain')))
        else:
            subdomain = Path(domain_dir/'no_sub_domain')
    else:
        domain_dir = Path(path/'no_domain')
        subdomain = domain_dir
    try:
        if not Path.exists(domain_dir):
            domain_dir.mkdir(parents=True)
        if not Path.exists(subdomain):
            subdomain.mkdir(parents=True)
    except Exception:
        pass
    save_path = Path(subdomain / 'articel').with_suffix('.json')
    with open(save_path, mode='a') as f:
        f.write(json.dumps(doc, ensure_ascii=False) + '\n')


def procss_per_file(file_path: Path, dir):
    x = 0
    with open(file_path) as f:
        for line in f:
            print(x)
            process_per_line(json.loads(line), dir)
            x += 1



# 测试
test_str = "Hello\n\nWorld"
print(replace_newlines(test_str))  # 输出：Hello\r\nWorld

def json_dir_to_file(json_dir: Path, save_dir:Path):
    for s in json_dir.glob('*.json'):
        procss_per_file(s, save_dir/s.stem)



if __name__ == '__main__':
    name = '2023-09-12'
    jons_dir = Path(f'/home/ptking/Documents/aliyun - imported on 2023年8月17日/mulwenben_{name}/jsons')
    save_dir = Path(f'/home/ptking/Documents/aliyun - imported on 2023年8月17日/mulwenben_{name}/res')
    json_dir_to_file(jons_dir, save_dir)
