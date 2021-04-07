import unittest
import homework


class TestHomework(unittest.TestCase):
    def setUp(self):
        homework.read_file("input1.txt")

    def tearDown(self):
        pass

    def test_has_predicate(self):
        func = homework.has_predicate
        self.assertFalse(func("~Ready(x)|~Ready(y)|Play(x,y)", "Play(Hayley,Teddy)"))

    def test_resolve(self):
        func = homework.resolve

    def test_replace_parameter(self):
        func = homework.replace_param
        self.assertEqual(func("Ready(x)", "x", "Teddy"), "Ready(Teddy)")
        self.assertEqual(func("Ready(y)", "x", "Teddy"), "Ready(y)")
        self.assertEqual(func("Play(x, y)", "x", "Teddy"), "Play(Teddy,y)")
        self.assertEqual(homework.replace_param("Play(x, y)", "y", "Teddy"), "Play(x,Teddy)")
