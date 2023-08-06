import math
from abc import abstractmethod


class VideoUtils:
    def __init__(self, video_source):
        self._duration = 0
        self._video_source = video_source or ''

    @abstractmethod
    def download(self):
        pass

    def generate_std_name(self):
        return f"{math.ceil(self._duration)}_{self._video_source.replace('/', '_').replace(':', '_').replace('.', '_')}.mp4"

    @abstractmethod
    def _get_duration(self) -> int:
        return self._duration

    @property
    def video_source(self):
        return self._video_source

    @property
    def save_dir(self):
        return self._save_dir

    @property
    def duration(self):
        return self._get_duration()


