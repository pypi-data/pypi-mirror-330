

from typing import Iterable, List


# Note that for the sequences to work the least significant bit
# always comes first.


def int_to_bit_sequence(value: int) -> List[bool]:
    return [
        bool(value & 0b00000001),
        bool(value & 0b00000010),
        bool(value & 0b00000100),
        bool(value & 0b00001000),
        bool(value & 0b00010000),
        bool(value & 0b00100000),
        bool(value & 0b01000000),
        bool(value & 0b10000000),
    ]


#def int_sequence_to_bit_sequence(values: Iterable[int]) -> List[bool]:
#    output = []
#    for value in values:
#        output.extend(int_to_bit_sequence(value))
#    return output


CHARS = "@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞ\x1bÆæßÉ !\"#¤%&'()*+,-./0123456789:;" \
        "<=>?¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ`¿abcdefghijklmnopqrstuvwxyzäöñüà"


def text_to_code_sequence(text: str) -> List[int]:
    output = []
    for char in text:
        code = CHARS.index(char)
        output.append(code)
    return output


def text_to_7bit_sequence(source: str) -> List[bool]:
    output = []
    for code in text_to_code_sequence(source):
        bits = int_to_bit_sequence(code)
        bits.pop(-1)  # turn 8 bits to 7
        output.extend(bits)
    return output


def bit_sequence_to_octet(bits: List[bool]) -> int:
    assert len(bits) == 8
    return sum((
        128 if bits[7] else 0,
        64 if bits[6] else 0,
        32 if bits[5] else 0,
        16 if bits[4] else 0,
        8 if bits[3] else 0,
        4 if bits[2] else 0,
        2 if bits[1] else 0,
        1 if bits[0] else 0,
    ))


def bit_sequence_to_octets(bits: List[bool]) -> List[int]:
    output = []
    source = list(bits)
    while len(source) > 0:
        if len(source) == 1:
            source.extend((False, False, False, True, True, False, True))
        while len(source) < 8:
            source.append(False)
        output.append(bit_sequence_to_octet(source[0:8]))
        source = source[8:]
    return output


def text_to_octets(text: str) -> List[int]:
    bits = text_to_7bit_sequence(text)
    return bit_sequence_to_octets(bits)
