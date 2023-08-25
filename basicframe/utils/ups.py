import json


def process_json_line(line):
    data = json.loads(line)

    content_url = data.get("内容直达链接（网址）")
    home_url = data.get("网站首页（网址）")
    if content_url and isinstance(content_url,

                                  str) and content_url != "NAN" and content_url != "/" and content_url.strip():
        data["start_url"] = content_url
    elif home_url and isinstance(home_url, str) and home_url != "NAN" and home_url != "/" and home_url.strip():
        data["start_url"] = home_url
        data['type'] = "full"
    else:
        data["start_url"] = 'null'
        data['type'] = 'null'
        data['status'] = 'error'

    return data


def update_start_url(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            updated_data = process_json_line(line.strip())
            updated_line = json.dumps(updated_data, ensure_ascii=False) + '\n'
            outfile.write(updated_line)


input_file_path = 'duoyuzhong_updated.txt'
output_file_path = 'duoyuzhong11.txt'
update_start_url(input_file_path, output_file_path)