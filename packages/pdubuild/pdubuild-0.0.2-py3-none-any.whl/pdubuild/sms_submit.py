

from dataclasses import dataclass
from enum import Enum
from typing import TextIO

from .util import digits_flipped_for_octets, encode_ucs2, encode_gsm7


class DataEncoding(Enum):
    UCS2 = (8, 67)
    #GSM7 = (0, 134)
    #GSM7 = (0, 160)
    GSM7 = (0, 152)

    def __init__(self, identifier: int, maxchunksize: int):
        self.identifier = identifier
        self.maxchunksize = maxchunksize

    @classmethod
    def from_alias(self, alias: str) -> "DataEncoding":
        if alias in ("ucs2",):
            return DataEncoding.UCS2
        elif alias in ("gsm7",):
            return DataEncoding.GSM7
        else:
            raise ValueError("Unknown encoding: %r" % alias)


@dataclass
class UserData:
    has_header: bool
    total_parts: int
    sequence_number: int
    encoding: DataEncoding
    message: str

    def __post_init__(self) -> None:
        if len(self.message) > self.encoding.maxchunksize:
            raise ValueError("Message too long for encoding format")

    def render_header(self) -> str:
        if not self.has_header:
            return ""
        header_body = "".join((
            self.render_concat_16bit_block(),
        ))
        header_body_len = len(header_body) // 2
        return ("%02X" % header_body_len) + header_body

    def render_concat_16bit_block(self) -> str:
        return "".join((
            "0804B49F",  # FIXME stuff
            "%02X" % self.total_parts,
            "%02X" % self.sequence_number,
        ))

    def render_body(self) -> str:
        if self.encoding is DataEncoding.UCS2:
            return encode_ucs2(self.message)
        elif self.encoding is DataEncoding.GSM7:
            return encode_gsm7(self.message)
        else:
            raise NotImplementedError(repr(self.encoding))

    def length(self) -> int:
        if self.encoding is DataEncoding.UCS2:
            return self.rendered_octet_length()
        elif self.encoding is DataEncoding.GSM7:
            header_septs = (len(self.render_header()) * 8) // 7 // 2
            return header_septs + len(self.message)
        else:
            raise NotImplementedError(repr(self.encoding))

    def rendered_octet_length(self) -> int:
        return (len(self.render_header()) + len(self.render_body())) // 2


@dataclass
class SmsSubmit:
    smsc: str
    dest: str
    userdata: UserData
    message_reference: int = 0
    reject_duplicates: bool = False
    status_report_request: bool = False
    reply_path: bool = False

    def status_octet(self) -> int:
        status = 1  # bits 0 and 1 indicate SMS-SUBMIT
        if self.reject_duplicates:
            status += 4
        status += 16  # assume relative validity FIXME
        if self.status_report_request:
            status += 32
        if self.userdata.has_header:
            status += 64
        if self.reply_path:
            status += 128
        return status

    def render_to(self, stream: TextIO) -> None:
        # Write the SMSC
        smsc_repr = digits_flipped_for_octets(self.smsc.lstrip("+"))
        stream.write("%02X" % ((len(smsc_repr) // 2) + 1))
        if self.smsc.startswith("+"):
            stream.write("91")
        else:
            stream.write("81")
        stream.write(smsc_repr)
        # Write the bitmask
        stream.write("%02X" % self.status_octet())
        # Write the message reference
        stream.write("%02X" % self.message_reference)
        # Write the destination
        stream.write("%02X" % len(self.dest.lstrip("+")))
        if self.dest.startswith("+"):
            stream.write("91")
        else:
            stream.write("81")
        stream.write(digits_flipped_for_octets(self.dest.lstrip("+")))
        # Write assorted metadata
        stream.write("00")  # TP-PID (protocol identifier)
        stream.write("%02X" % self.userdata.encoding.identifier)
        stream.write("FF")  # Maximum validity
        # Write the message
        stream.write("%02X" % self.userdata.length())
        stream.write(self.userdata.render_header())
        stream.write(self.userdata.render_body())
