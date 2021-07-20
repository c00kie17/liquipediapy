import unittest
from liquipediapy.liquipediapy import liquipediapy
from liquipediapy.exceptions import RequestsException


class LiquipediaTestsParse(unittest.TestCase):
    def setUp(self):
        self.liq_obj = liquipediapy("appname", "dota2")

    def test_parse_pass(self):
        parsed_page = self.liq_obj.parse("Arteezy")
        self.assertIsNotNone(parsed_page)

    def test_parse_fail(self):
        with self.assertRaises(RequestsException) as context:
            self.liq_obj.parse("Ateezy")


class LiquipediaTestsSearch(unittest.TestCase):
    def setUp(self):
        self.liq_obj = liquipediapy("appname", "dota2")

    def test_search_pass(self):
        search_result = self.liq_obj.search("mar")
        self.assertIsNotNone(search_result)


if __name__ == "__main__":
    unittest.main()