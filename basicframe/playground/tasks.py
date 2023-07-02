import asyncio
import subprocess
from celery import Celery

# 创建 Celery 应用
app = Celery('myapp', broker='redis://:Liupeitao1.@106.15.10.74:6379/0')
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



def download_m3u8(m3u8_url, path):
    command = f'ffmpeg -i {m3u8_url} -c copy  {path}'
    command = ['ffmpeg', '-i', f'{m3u8_url}', '-c', 'copy', f'{path}']
    print(f'开始下载——{path}')
    result = subprocess.check_output(command).decode('utf-8')
    return result



# def get_m3u8_duration(m3u8_url):
#     print(m3u8_url)
#     loop = asyncio.get_event_loop()
#     async def run_command():
#         command = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
#                    'default=noprint_wrappers=1:nokey=1', '-i', m3u8_url]
#         process = await asyncio.create_subprocess_exec(*command, stdout=asyncio.subprocess.PIPE,
#                                                        stderr=asyncio.subprocess.PIPE)
#         stdout, stderr = await process.communicate()
#         print(process.returncode)
#         print(stdout.decode())
#         print(stderr.decode())
#         return stdout.decode()
#
#     result = loop.run_until_complete(run_command())
#     return result
#
