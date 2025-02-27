

import argparse

from . import build


def main() -> None:
    parser = argparse.ArgumentParser(prog="pdubuild")
    parser.add_argument("charset", choices=["gsm7", "ucs2"])
    parser.add_argument("smsc")
    parser.add_argument("destination")
    parser.add_argument("message")
    args = parser.parse_args()
    pdus = list(build(args.smsc, args.destination, args.message, args.charset))
    for pdu in pdus:
        print(pdu)
