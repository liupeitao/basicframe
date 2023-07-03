import json
import os
import re
import subprocess

import yt_dlp

from basicframe.utils.decorator import execution_time, log


class Downloader:
    def __init__(self):
        pass

    @staticmethod
    def get_video_info( url):
        pass

    @staticmethod
    def download_video( url, output_dir='.'):
        pass

    @staticmethod
    @log
    @execution_time
    def get_duration(url):
        pass


class YtDlpDownloader(Downloader):
    @staticmethod
    def get_video_info(url):
        ydl_opts = {
            'dump_single_json': True,
            'extract_flat': 'in_playlist',
            'simulate': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
        return info_dict

    @staticmethod
    def download_video(url, output_dir='.'):
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f'{output_dir}_%(title)s_.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    @staticmethod
    def get_duration(url):
        try:
            video_info = str(YtDlpDownloader.get_video_info(url))
            duration = re.findall(r"'duration': (\d*\.?\d*)", video_info)[0]
            return duration
        except KeyError as e:
            print('yt-dlp no duration key')
            return 0


class YouGetDownloader(Downloader):
    @staticmethod
    def get_video_info(url):
        command = ['you-get', '-i', f'{url}']
        output = subprocess.check_output(command, encoding='utf-8')
        return output

    @staticmethod
    def download_video(url, output_dir='./'):
        command = ['you-get','-o', os.path.join(output_dir, url), f'{url}']
        output = subprocess.check_output(command, encoding='utf-8')

    @staticmethod
    def get_duration(url):
        return 0


# if __name__ == '__main__':
#     print(YtDlpDownloader.get_video_info('https://www.bilibili.com/video/BV1ns4y1F7EQ/?spm_id_from=333.1007.0.0'))
