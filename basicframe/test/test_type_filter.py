import unittest

from basicframe.filters.filter import FilterChain, PartialStaticPageSiteFilter, FullSiteFilter


# Mocking the functions for testing purposes


class TestFilterChain(unittest.TestCase):
    def setUp(self):
        self.chain = FilterChain()
        self.chain.add_filter(PartialStaticPageSiteFilter()).add_filter(FullSiteFilter())

    def test_partial_static_page_filter(self):
        response = self.chain.do_filter("https://rtrp.jp/articles/104079/", None)
        self.chain.reset()
        self.assertEqual(response, 'psp_type')

    def test_full_site_filter(self):
        response = self.chain.do_filter("https://www.noticiasaominuto.com/casa", None)
        self.chain.reset()
        self.assertEqual(response, 'full_type')



if __name__ == "__main__":
    unittest.main()
