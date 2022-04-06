import json
from dataclasses import dataclass

from src.lib.sides.exchange.steps import ProtocolSteps

ENCODING = 'UTF-8'


@dataclass
class Message:
    step: ProtocolSteps
    data: dict = None

    def __bytes__(self):
        return json.dumps({
            'step': self.step.value,
            'data': self.data
        }).encode(encoding=ENCODING)

    @staticmethod
    def from_bytes(pack: bytes) -> 'Message':
        msg = json.loads(pack.decode(encoding=ENCODING))
        return Message(
            ProtocolSteps(msg['step']),
            msg['data']
        )
