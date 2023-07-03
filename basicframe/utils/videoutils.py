from basicframe.utils.decorator import execution_time, log

import math
class VideoUtils:
    def __init__(self, path_id, source, save_dir):
        self._duration = 0
        self._path = path_id or ''
        self._source = source
        self._save_dir = save_dir or ''

    def download(self):
        pass

    def generate_std_name(self):
        return f"{self.source}_{math.ceil(self.duration())}_{self.path.replace('/', '_').replace(':', '_').replace('.', '_')}.mp4"

    def duration(self):
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


