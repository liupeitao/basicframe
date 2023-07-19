import asyncio
import subprocess
import time

# 控制并发数为100
semaphore = asyncio.Semaphore(100)
from basicframe.midwares.redisclient import RedisClient

redis_conn = RedisClient().connect()


def generate_std_filename(website_name, duration, key_or_other):
    filename = f'{website_name}_{duration}_' + key_or_other.replace('/', '_').replace(':', '_').replace('.',
                                                                                                        '_') + '.mp4'
    return filename


async def get_m3u8_duration(m3u8_url):
    async with semaphore:
        print(m3u8_url)

        # m3u8_url = 'https://v5.cdtlas.com/20220619/6hCH3rE1/index.m3u8'
        command = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                   'default=noprint_wrappers=1:nokey=1', '-i', m3u8_url]

        process = await asyncio.create_subprocess_exec(*command, stdout=asyncio.subprocess.PIPE,
                                                       stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()
        print(process.returncode)
        print(stdout.decode())
        print(stderr.decode())


async def download_m3u8_video(m3u8_url, path):
    print('正在下载视频: ', m3u8_url)
    try:
        command = f'ffmpeg -y -i {m3u8_url} -c copy {path}'
        process = await asyncio.create_subprocess_shell(command)
        await process.wait()
        print(f'Successfully downloaded M3U8 video and saved as {path}.')
    except subprocess.CalledProcessError as e:
        print(e)
        raise Exception


async def task(url):
    m3u8_url = 'https://v5.cdtlas.com/20220619/6hCH3rE1/index.m3u8'
    print(url)


m_list = redis_conn.lrange('kmj_valid_m3u8', 0, 100)
for m3u8 in m_list:
    print(m3u8)


async def main():
    tasks = [get_m3u8_duration(i) for i in m_list]
    # await asyncio.gather(*tasks)
    await asyncio.wait(tasks)


start = time.time()
asyncio.run(main())
end = time.time()
print(end - start)
