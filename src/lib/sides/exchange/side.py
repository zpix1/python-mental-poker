from typing import Dict, List

from src.lib.sides.communication.communicator import Communicator
from src.lib.sides.exchange.exchangeexception import ExchangeException
from src.lib.sides.exchange.message import Message
from src.lib.sides.exchange.steps import ProtocolSteps


class Side:
    communicator: Communicator
    deck: List[str]

    def __init__(self, communicator: Communicator):
        self.communicator = communicator

    def send_message(self, message: Message) -> None:
        return self.communicator.send_bytes(bytes(message))

    def receive_message(self) -> Message:
        return Message.from_bytes(self.communicator.receive_bytes())

    def receive_message_of_step(self, step: ProtocolSteps) -> Message:
        message = self.receive_message()
        if message.step != step:
            self.send_message(Message(ProtocolSteps.ABORT))
            raise ExchangeException(f'Wrong type of message: {step.value} expected, {message.step.value} actual')
        return message

    def assert_or_abort(self, value: bool, message: str = '') -> None:
        if not value:
            self.send_message(Message(ProtocolSteps.ABORT))
            raise ExchangeException(f'Assert or abort: got false value, {message}')

    @staticmethod
    def convert_deck_to_strings(deck: List[int], strings: Dict[str, int]):
        swapped = dict((v, k) for k, v in strings.items())
        return list([swapped[v] for v in deck])

    def get_deck(self):
        return self.deck
