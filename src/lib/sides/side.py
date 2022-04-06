from src.lib.sides.communication.communicator import Communicator
from src.lib.sides.exchangeexception import ExchangeException
from src.lib.sides.message import Message
from src.lib.sides.steps import ProtocolSteps


class Side:
    communicator: Communicator

    def __init__(self, communicator: Communicator):
        self.communicator = communicator

    def send_message(self, message: Message) -> None:
        return self.communicator.send_bytes(bytes(message))

    def receive_message(self) -> Message:
        return Message.from_bytes(self.communicator.receive_bytes())

    def receive_message_of_step(self, step: ProtocolSteps) -> Message:
        message = self.receive_message()
        if message.step != step:
            raise ExchangeException(f'Wrong type of message: {step.value} expected, {message.step.value} actual')
        return message
