import logging

from src.lib.sides.communication.communicator import Communicator


class FakeCommunicator(Communicator):
    def send_bytes(self, message: bytes) -> None:
        logging.debug(f'Sent a message {message}')

    def receive_bytes(self) -> bytes:
        logging.debug('Tried to receive a message')
        return b''
