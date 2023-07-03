import os
import subprocess
from basicframe.midware.redisclient import RedisClient
from basicframe.utils.decorator import log, execution_time
from basicframe.utils.videoutils import VideoUtils

redis_conn = RedisClient().connect()


class M3u8Utils(VideoUtils):
    def __init__(self, path_id, source, save_dir):
        super().__init__(path_id, source, save_dir)

    def duration(self):
        if self._duration != 0:
            return self._duration
        m3u8_url = self.path
        command = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                   'default=noprint_wrappers=1:nokey=1', '-i', m3u8_url]
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, timeout=300000).decode(
                'utf-8').strip()
            duration = float(output)
            self._duration = duration
            print(duration)
            return duration
        except Exception as e:
            print(e.args, e)
            return 0

    def download(self):
        print('正在下载视频: ', self._path)
        save_path = os.path.join(self.save_dir, self.generate_std_name())
        command = ['ffmpeg', '-y', '-i', f'{self.path}', '-c', 'copy', f'{save_path}']
        try:
            subprocess.check_output(command)
            print(f'Successfully downloaded M3U8 video and saved as {save_path}.')
        except subprocess.CalledProcessError as e:
            print(e)
            raise Exception

    def generate_std_name(self):
        return super().generate_std_name()


# if __name__ == '__main__':
#     for i in redis_conn.lrange('not_down', 0, 10):
#         video_util = M3u8Utils('https://v4.cdtlas.com/20220612/cfk1lDBj/index.m3u8', 'kmj',
#                            '/home/liupeitao/PycharmProjects/basicframe/basicframe/assets/videos/ru')
#         print(video_util.download())
#
