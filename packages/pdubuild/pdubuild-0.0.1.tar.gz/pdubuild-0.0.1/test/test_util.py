

import unittest

from pdubuild import util


class TestDigitFlipping(unittest.TestCase):

    def test_even(self):
        result = util.digits_flipped_for_octets("123456")
        self.assertEqual(result, "214365")

    def test_odd(self):
        result = util.digits_flipped_for_octets("12345")
        self.assertEqual(result, "2143F5")
