import logging

from src.lib.crypto.utils import encrypt
from src.lib.sides.communication.communicator import Communicator
from src.lib.crypto.cryptodata import CryptoData
from src.lib.sides.message import Message
from src.lib.sides.side import Side
from src.lib.sides.steps import ProtocolSteps


class ExchangeClient(Side):
    def trade(self, crypto_data: CryptoData):
        logging.info(f'Starting a new exchange {crypto_data.N = }, {crypto_data.k = }')

        logging.info('Sending hello to server')
        self.send_message(Message(ProtocolSteps.HELLO))

        encrypted_deck = [encrypt(crypto_data, v) for v in crypto_data.strings.values()]

        logging.info('Sending crypto values and deck to server')
        self.send_message(Message(ProtocolSteps.CRYPTO_VALUES_AND_DECK, {
            "N": crypto_data.N,
            "k": crypto_data.k,
            "p": crypto_data.p,
            "strings": crypto_data.strings,
            "deck": encrypted_deck
        }))

        logging.info('Sending ')
