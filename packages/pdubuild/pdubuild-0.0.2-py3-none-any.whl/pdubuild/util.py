

from .bitting import text_to_octets


def digits_flipped_for_octets(digits: str) -> str:
    digits_in, digits_out = list(digits), []
    while len(digits_in) > 0:
        first = digits_in.pop(0)
        if len(digits_in) > 0:
            second = digits_in.pop(0)
        else:
            second = "F"
        digits_out.append(second)
        digits_out.append(first)
    return "".join(digits_out)


def encode_ucs2(text: str) -> str:
    return text.encode("utf_16_be").hex().upper()


def encode_gsm7(text: str) -> str:
    return "".join("%02X" % x for x in text_to_octets(text))
