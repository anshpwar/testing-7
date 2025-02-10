import unittest

from lmskit import calc


class CalcTests(unittest.TestCase):
    def test_combined_charge(self):
        self.assertEqual(calc.combined_charge(0), 50)
        self.assertEqual(calc.combined_charge(1), 50)
        self.assertEqual(calc.combined_charge(2), 70)
        self.assertEqual(calc.combined_charge(3), 70)
