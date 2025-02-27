

from typing import Iterator, List
import io

from .sms_submit import DataEncoding, UserData, SmsSubmit


__version__ = "0.0.1"


def split(chunksize: int, source: str) -> List[str]:
    output = []
    i = 0
    while i < len(source):
        output.append(source[i:(i + chunksize)])
        i += chunksize
    return output


def build(
        smsc: str,
        dest: str,
        message: str,
        encodewith: str,
) -> Iterator[str]:
    encoding = DataEncoding.from_alias(encodewith)
    chunks = split(encoding.maxchunksize, message)
    for i, chunk in enumerate(chunks):
        output = io.StringIO()
        has_header = (encodewith == "ucs2") or (len(chunks) > 1)  # somewhat bodgy!
        userdata = UserData(total_parts=len(chunks), sequence_number=(i + 1),
                            encoding=encoding, message=chunk, has_header=has_header)
        sms_submit = SmsSubmit(smsc=smsc, dest=dest, userdata=userdata)
        sms_submit.render_to(output)
        yield output.getvalue()
