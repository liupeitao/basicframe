import os
import subprocess

from basicframe.utils.videoutils import VideoUtils


class M3u8Utils(VideoUtils):
    def __init__(self, video_source, website):
        super().__init__(video_source)
        self._website = website

    def _get_duration(self):
        if self._duration != 0:
            return self._duration
        m3u8_url = self._video_source
        command = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                   'default=noprint_wrappers=1:nokey=1', '-i', m3u8_url]
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, timeout=300000).decode(
                'utf-8').strip()
            duration = float(output)
            self._duration = duration
            return self._duration
        except Exception as e:
            print(e.args, e)
            return 0

    def download(self, save_dir):
        print('正在下载视频: ', self._video_source)
        save_path = os.path.join(save_dir, self.generate_std_name())
        command = ['ffmpeg', '-y', '-i', f'{self._video_source}', '-c', 'copy', f'{save_path}']
        try:
            subprocess.check_output(command)
            print(f'Successfully downloaded M3U8 video and saved as {save_path}.')
        except subprocess.CalledProcessError as e:
            print(e)
            raise Exception

    def generate_std_name(self):
        return self._website + "_" + super().generate_std_name()  # 非瓶颈无需优化


if __name__ == '__main__':
    video_util = M3u8Utils('https://v4.cdtlas.com/20220612/cfk1lDBj/index.m3u8', 'kmj')
    print(video_util.generate_std_name())
