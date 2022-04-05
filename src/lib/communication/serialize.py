import json

ENCODING = 'UTF-8'


def serialize_message(payload: dict) -> bytes:
    return json.dumps(payload).encode(encoding=ENCODING)


def parse_message(data: bytes) -> dict:
    return json.loads(data.decode(encoding=ENCODING))
