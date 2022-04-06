from src.lib.sides.side import Side
from src.lib.sides.steps import ProtocolSteps


class ExchangeServer(Side):
    def wait_for_connection(self):
        self.receive_message_of_step(ProtocolSteps.HELLO)

