import math
import random
from abc import abstractmethod


class VideoUtils:
    def __init__(self, path_id=random.randint(0, 100000), source='tmp', save_dir='/tmp'):
        self._duration = 0
        self._path = path_id or ''
        self._source = source
        self._save_dir = save_dir or ''

    @abstractmethod
    def download(self):
        pass

    def generate_std_name(self):
        return f"{self.source}_{math.ceil(self.get_duration())}_{self.path.replace('/', '_').replace(':', '_').replace('.', '_')}.mp4"

    def get_duration(self):
        return self._duration

    @property
    def path(self):
        return self._path

    @property
    def source(self):
        return self._source

    @property
    def save_dir(self):
        return self._save_dir

    @property
    def duration(self):
        return self._duration
