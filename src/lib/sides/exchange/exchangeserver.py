import logging
from typing import List

from Crypto.Random.random import sample, shuffle

from src.lib.crypto.cryptodata import CryptoData
from src.lib.crypto.utils import encrypt, decrypt
from src.lib.sides.exchange.message import Message
from src.lib.sides.exchange.side import Side
from src.lib.sides.exchange.steps import ProtocolSteps


class ExchangeServer(Side):
    client_crypto_values: dict
    client_encrypted_deck: List[int]

    def wait_for_connection_and_crypto_values(self):
        self.receive_message_of_step(ProtocolSteps.HELLO)
        values_msg = self.receive_message_of_step(ProtocolSteps.CRYPTO_VALUES_AND_DECK)
        logging.debug(f'Got a new connection with crypto values {values_msg.data}')
        self.client_crypto_values = values_msg.data
        return values_msg.data

    def continue_communication(self, c: int, d: int):
        crypto_data = CryptoData(
            N=self.client_crypto_values['N'],
            k=self.client_crypto_values['k'],
            strings=self.client_crypto_values['strings'],
            p=self.client_crypto_values['p'],
            c=c,
            d=d,
        )

        self.assert_or_abort(
            len(self.client_crypto_values['deck']) == crypto_data.N,
            'Wrong deck size'
        )

        encrypted_deck = self.client_crypto_values['deck']
        shuffle(encrypted_deck)
        encrypted_client_deck, encrypted_deck_end = encrypted_deck[:crypto_data.k], encrypted_deck[crypto_data.k:]

        double_encrypted_deck_end = list([encrypt(crypto_data, v) for v in encrypted_deck_end])

        self.send_message(Message(ProtocolSteps.CLIENT_DECK_AND_DOUBLE_ENCRYPTED_END, {
            'encrypted_client_deck': encrypted_client_deck,
            'double_encrypted_deck_end': double_encrypted_deck_end
        }))

        encrypted_server_deck_msg = self.receive_message_of_step(ProtocolSteps.SERVER_DECK)

        encrypted_server_deck = encrypted_server_deck_msg.data['encrypted_server_deck']
        self.assert_or_abort(
            len(encrypted_server_deck) == crypto_data.k,
            'Wrong encrypted server deck size'
        )

        server_deck = list([decrypt(crypto_data, v) for v in encrypted_server_deck])

        for card in server_deck:
            if card not in crypto_data.strings.values():
                self.assert_or_abort(False, f'card value {card} not in deck')

        self.deck = self.convert_deck_to_strings(server_deck, crypto_data.strings)
        logging.info(f'Got server deck {self.deck}')

        logging.debug('Ending exchange')
        self.send_message(Message(ProtocolSteps.END))
