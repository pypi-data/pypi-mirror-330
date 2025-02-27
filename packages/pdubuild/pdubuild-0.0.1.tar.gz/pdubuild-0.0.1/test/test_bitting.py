

import unittest


from pdubuild import bitting


class TestBitification(unittest.TestCase):

    def test_int(self):
        bits = bitting.int_to_bit_sequence(84)
        self.assertEqual(bits, [
            False, False, True, False, True, False, True, False,
        ])

    #def test_sequence(self):
    #    bits = bitting.int_sequence_to_bit_sequence([84, 7, 13])
    #    self.assertEqual(bits, [
    #        False, True, False, True, False, True, False, False,
    #        False, False, False, False, False, True, True, True,
    #        False, False, False, False, True, True, False, True,
    #    ])

    def test_7bit_text(self):
        bits = bitting.text_to_7bit_sequence("Hello")
        self.assertEqual(bits, [
            False, False, False, True, False, False, True,
            True, False, True, False, False, True, True,
            False, False, True, True, False, True, True,
            False, False, True, True, False, True, True,
            True, True, True, True, False, True, True,
        ])


class TestCodes(unittest.TestCase):

    def test_text(self):
        codes = bitting.text_to_code_sequence("Hello")
        self.assertEqual(codes, [0x48, 0x65, 0x6c, 0x6c, 0x6f])

    def test_failure(self):
        with self.assertRaises(ValueError):
            bitting.text_to_code_sequence("foo\tbar")


class TestOctetting(unittest.TestCase):

    def test_one_octet(self):
        bits = [True, True, True, False, False, True, True, False]
        self.assertEqual(bitting.bit_sequence_to_octet(bits), 103)

    def test_text_one(self):
        octets = bitting.text_to_octets("Hello the")
        self.assertEqual(octets, [0xC8, 0x32, 0x9b, 0xFD, 0x06, 0xD1, 0xD1, 0x65])

    def test_text_longer(self):
        octets = bitting.text_to_octets("Hello there seven bit version local dest  ")
        rendered = "".join("%02X" % octet for octet in octets)
        self.assertEqual(rendered, "C8329BFD06D1D1657919342FDBCB6E90384D07D9CBF27"
                                   "9FAED06B1DFE3301B442ECFE92010")
