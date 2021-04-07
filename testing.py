import unittest
import homework


class TestHomework(unittest.TestCase):
    def setUp(self):
        homework.read_file("input1.txt")

    def tearDown(self):
        pass

    def test_has_neg_predicate(self):
        func = homework.has_neg_predicate
        self.assertFalse(func("~Ready(x)|~Ready(y)|Play(x,y)", "Play(Teddy, Hayley)"))
        self.assertTrue(func("~Ready(x)|~Ready(y)|Play(x,y)", "~Play(Hayley, Teddy)"))
        self.assertTrue(func('~Start(x)|~Healthy(x)|Ready(x)', 'Healthy(Teddy)'))

    def test_resolve(self):
        func = homework.resolve
        self.assertEqual("~Ready(Hayley)|~Ready(Teddy)",
                         func("~Ready(x)|~Ready(y)|Play(x,y)", "~Play(Hayley, Teddy)"))
        self.assertEqual(None,
                         func("~Ready(x)|~Ready(y)|Play(Tim,y)", "~Play(Hayley, Teddy)"))
        self.assertEqual("~Start(Hayley)",
                         func("~Start(x)|Healthy(x)", "~Healthy(Hayley)"))

    def test_replace_parameter(self):
        func = homework.replace_param
        self.assertEqual(func("Ready(x)", "x", "Teddy"), "Ready(Teddy)")
        self.assertEqual(func("Ready(y)", "x", "Teddy"), "Ready(y)")
        self.assertEqual(func("Play(x, y)", "x", "Teddy"), "Play(Teddy,y)")
        self.assertEqual(func("Play(x, y)", "y", "Teddy"), "Play(x,Teddy)")
