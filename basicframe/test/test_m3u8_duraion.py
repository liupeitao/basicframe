import pytest

from basicframe.utils.m3u8videoutils import M3u8Utils


@pytest.fixture
def your_object():
    # 创建被测试的对象实例
    your_object = M3u8Utils('https://v4.cdtlas.com/20220611/iLLRWxxK/index.m3u8', 'kmj', '/tmp')
    return your_object


def test_duration_with_valid_url(your_object):
    # 使用有效的 M3U8 URL 测试 duration 方法
    duration = your_object.get_duration()
    assert isinstance(duration, float)
    assert duration > 0


def test_duration_with_invalid_url(your_object):
    # 使用无效的 M3U8 URL 测试 duration 方法
    your_object._path = 'invalid_url.m3u8'
    duration = your_object.get_duration()
    assert duration == 0


def test_duration_with_empty_path(your_object):
    # 使用空路径测试 duration 方法
    your_object._path = ''
    duration = your_object.get_duration()
    assert duration == 0
