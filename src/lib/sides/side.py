from src.lib.sides.communication.communicator import Communicator
from src.lib.sides.communication.serialize import serialize_message, parse_message
from src.lib.sides.steps import ProtocolSteps


class Side:
    communicator: Communicator

    def __init__(self, communicator: Communicator):
        self.communicator = communicator

    def send_message(self, step: ProtocolSteps, data: dict = None) -> None:
        return self.communicator.send_bytes(serialize_message({
            "step": step.value,
            "data": data
        }))

    def receive_message(self) -> (ProtocolSteps, dict):
        msg = parse_message(self.communicator.receive_bytes())
        return ProtocolSteps(msg['step']), msg['data']
