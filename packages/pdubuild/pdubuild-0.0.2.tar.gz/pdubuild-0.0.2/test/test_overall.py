

import unittest

from pdubuild import build


class TestExample(unittest.TestCase):

    def test_single_ucs2(self):
        pdus = list(build(
            smsc="+447785016005",
            dest="07493574689",
            message="f0 Hi John it's me",
            encodewith="ucs2",
        ))
        self.assertEqual(pdus, [
            # One PDU:
            "079144775810065051000B817094534786F90008FF2B0"
            "60804B49F0101006600300020004800690020004A006F"
            "0068006E002000690074002700730020006D0065"
        ])

    def test_single_gsm7(self):
        pdus = list(build(
            smsc="+447785016005",
            dest="07493574689",
            message="Hello there seven bit version local dest  ",
            encodewith="gsm7",
        ))
        self.assertEqual(pdus, [
            # One PDU:
            "079144775810065011000B817094534786F90000FF2AC"
            "8329BFD06D1D1657919342FDBCB6E90384D07D9CBF279"
            "FAED06B1DFE3301B442ECFE92010"
        ])

    def test_multipart_ucs2(self):
        # Awkwardly abridged... we only have 2 of the three parts
        message = (
            "It is an ancient Mariner,\r\n"
            "And he stoppeth one of three.\r\n"
            "'By thy long grey beard and glittering eye,\r\n"
            "Now wherefore stopp'st thou me?\r\n"
            "\r\n"
            "The Bridegroom's doors are opened wide,\r\n"
            "And I am next of kin;\r\n"
            "The guests are met, the feast is set:\r\n"
            "May'st hear the merry din.'\r\n"
            "\r\n"
            "He holds him with his skinny han"
            #"He holds him with his skinny hand,\r\n"
            #"'There was a ship,' quoth he.\r\n"
            #"'Hold off! unhand me, grey-beard loon!'\r\n"
            #"Eftsoons his hand dropt he.\r\n"
        )
        pdus = list(build(
            smsc="+447785016005",
            dest="+447493574689",
            message=message,
            encodewith="gsm7",
        ))
        self.assertEqual(pdus, [
            # First PDU:
            "079144775810065051000C914447397564980000FFA00"
            #"60804B49F0301493A283D0785DDA0B07B9C2EBBE9A066"
            "60804B49F0201493A283D0785DDA0B07B9C2EBBE9A066"
            "589E7697E5AC8622E82683D065D09CFE86C3CB7434E8E"
            "D2E83DE66101D2D2F975D0DC5499807D1D17910FBED3E"
            "83CEF2721E242E87E56450D84D069DD9693ABD2C4FBBC"
            "FA072BECC6A289CEF3BE88E2ECBCBE6B7BC0C9AD3DF70"
            "F8694E07D1D1EF3AA85DFE35140D05155D0609E56972F"
            "92C7FBFDB",
            # Second PDU:
            "079144775810065051000C914447397564980000FFA00"
            #"60804B49F0302A73988FC7ECBE7A0B0BC0C7AC3CBEE32"
            "60804B49F0202A73988FC7ECBE7A0B0BC0C7AC3CBEE32"
            "19744F93CBAC8622E8268392A0701BE42EE3E9A0B719B"
            "44EBB770D05155D069DEBE5397D0E0ACBCBA07699CE02"
            "D1D16590B91C9ED341E939685EA6EB1A8A66387F9AD34"
            "1E872580EA2A3CBA076592ECF83C869B7EBD4503414C8"
            "3208FD6693E72074BA0DBAA7E968103A3D07CDD769B73"
            "B0F4287DD",
        ])
