import subprocess
from celery import Celery

from basicframe.utils.m3u8videoutils import M3u8Utils
# 创建 Celery 应用
app = Celery('myapp', broker='redis://:Liupeitao1.@106.15.10.74:6379/1')
# 配置 Celery
app.conf.update(
    result_backend='redis://:Liupeitao1.@106.15.10.74:6379/13',  # Redis URL
)


def get_m3u8_duration(m3u8_url):
    print(m3u8_url)
    command = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
               'default=noprint_wrappers=1:nokey=1', '-i', m3u8_url]
    result = subprocess.check_output(command).decode('utf-8')
    return result


# 定义任务函数
@app.task
def get_m3u8_duration_task(m3u8_url, i):
    result = get_m3u8_duration(m3u8_url)
    print(result, '-------------', i)
    return result


@app.task
def down_m3u8_task(m3u8_url, path):
    result = download_m3u8(m3u8_url, f'/tmp/{path}.mp4')
    return result


@app.task
def html_video_download_task(url):
    video =M3u8Utils(path=url, source='ru', save_dir='/home/liupeitao/PycharmProjects/basicframe/basicframe/assets/videos/ru')
    video.download()




def download_m3u8(m3u8_url, path):
    command = f'ffmpeg -i {m3u8_url} -c copy  {path}'
    command = ['ffmpeg', '-i', f'{m3u8_url}', '-c', 'copy', f'{path}']
    print(f'开始下载——{path}')
    result = subprocess.check_output(command).decode('utf-8')
    return result
