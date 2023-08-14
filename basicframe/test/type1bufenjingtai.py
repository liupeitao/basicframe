import unittest

from basicframe.midwares.redisclient import RedisClient


class MyTestCase(unittest.TestCase):
    def test_static_part_site(self):
        conn = RedisClient().connect()
        url_list = conn.lrange('静态部分网站', 0, -1)
        print(url_list)
if __name__ == '__main__':
    unittest.main()
