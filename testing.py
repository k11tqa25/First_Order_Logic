import unittest
import homework


class TestHomework(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_has_predicate(self):
        func = homework.has_predicate
        self.assertTrue(func())