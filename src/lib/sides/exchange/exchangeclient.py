import logging

from Crypto.Random.random import shuffle, choice

from src.lib.crypto.utils import encrypt, decrypt
from src.lib.crypto.cryptodata import CryptoData
from src.lib.sides.exchange.message import Message
from src.lib.sides.exchange.side import Side
from src.lib.sides.exchange.steps import ProtocolSteps


class ExchangeClient(Side):
    def trade(self, crypto_data: CryptoData):
        logging.debug(f'Starting a new exchange {crypto_data.N = }, {crypto_data.k = }')

        logging.debug('Sending hello to server')
        self.send_message(Message(ProtocolSteps.HELLO))

        encrypted_deck = list([encrypt(crypto_data, v) for v in crypto_data.strings.values()])
        shuffle(encrypted_deck)

        logging.debug(f'Sending crypto values and deck to server {encrypted_deck}')
        self.send_message(Message(ProtocolSteps.CRYPTO_VALUES_AND_DECK, {
            "N": crypto_data.N,
            "k": crypto_data.k,
            "p": crypto_data.p,
            "strings": crypto_data.strings,
            "deck": encrypted_deck
        }))

        client_deck_msg = self.receive_message_of_step(ProtocolSteps.CLIENT_DECK_AND_DOUBLE_ENCRYPTED_END)
        encrypted_client_deck = client_deck_msg.data['encrypted_client_deck']

        logging.debug(f'Got encrypted client deck: {encrypted_client_deck}')

        self.assert_or_abort(
            len(encrypted_client_deck) == crypto_data.k,
            'Client deck of wrong size'
        )

        client_deck = list([decrypt(crypto_data, v) for v in encrypted_client_deck])

        for card in client_deck:
            if card not in crypto_data.strings.values():
                self.assert_or_abort(False, f'card value {card} not in deck')

        logging.info(f'Got client deck: {self.convert_deck_to_strings(client_deck, crypto_data.strings)}')

        double_encrypted_deck_end = client_deck_msg.data['double_encrypted_deck_end']

        self.assert_or_abort(
            len(double_encrypted_deck_end) == crypto_data.N - crypto_data.k,
            'Deck end of wrong size'
        )

        shuffle(double_encrypted_deck_end)

        double_encrypted_server_deck, house_cards = double_encrypted_deck_end[
                                                    :crypto_data.k], double_encrypted_deck_end[crypto_data.k:]

        encrypted_server_deck = list([decrypt(crypto_data, v) for v in double_encrypted_server_deck])

        logging.debug(f'Sending encrypted server deck {encrypted_server_deck}')

        self.send_message(Message(ProtocolSteps.SERVER_DECK, {
            'encrypted_server_deck': encrypted_server_deck
        }))

        self.receive_message_of_step(ProtocolSteps.END)
        logging.debug('Ended')
