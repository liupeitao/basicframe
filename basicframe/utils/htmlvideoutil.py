import asyncio

from basicframe.utils.downloader import Downloader, YtDlpDownloader, YouGetDownloader
from basicframe.utils.videoutils import VideoUtils


class HtmlVideoUtil(VideoUtils):
    def __init__(self, path_id, source, save_dir, downloader=YtDlpDownloader()):
        super().__init__(path_id, source, save_dir)
        self.downloader = downloader

    def duration(self):
        if self._duration != 0:
            return self._duration
        try:
            url = self.path
            duration = self.downloader.get_duration(url)
            self._duration = duration
            return duration
        except Exception as e:
            print('no duration')
            return 0

    @property
    def path(self):
        return self._path

    def download(self):
        self.downloader.download_video(self.path, output_dir=self.generate_std_name())

    def get_video_info(self):
        return self.downloader.get_video_info(self.path)

    def generate_std_name(self):
        return super().generate_std_name()

# if __name__ == '__main__':
#     ytdlp = YtDlpDownloader()
#     html = HtmlVideoUtil('https://www.bilibili.com/video/BV12u4y1d717/?spm_id_from=333.1007.tianma.1-2-2.click', 'bilibili', './')
#     print(html.duration())
