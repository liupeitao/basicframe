import unittest

from basicframe.filters.filter import FilterChain, PartialStaticPageSiteFilter, FullSiteFilter


# Mocking the functions for testing purposes


class TestFilterChain(unittest.TestCase):

    def setUp(self):
        self.chain = FilterChain()
        self.chain.add_filter(PartialStaticPageSiteFilter()).add_filter(FullSiteFilter())

    def test_partial_static_page_filter(self):
        response = self.chain.do_filter("https://www.daily.co.jp/ring/", None)
        self.chain.reset()
        self.assertEqual(response, 'psp_type')

    def test_full_site_filter(self):
        response = self.chain.do_filter("https://pantip.com/profile/5160452#topic", None)
        self.chain.reset()
        self.assertEqual(response, 'full_type')

    def test_no_filter_match(self):
        response = self.chain.do_filter("https://pantip.com/profile/5160452#topic", None)
        self.chain.reset()
        self.assertFalse(response)

if __name__ == "__main__":
    unittest.main()
