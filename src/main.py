import logging
import random
from threading import Thread
from typing import List

from src.lib.crypto.cryptodata import CryptoData
from src.lib.crypto.utils import get_p, get_cd, seed_deck_values
from src.lib.sides.communication.streamcommunicator import StreamCommunicator
from src.lib.sides.exchange.exchangeclient import ExchangeClient
from src.lib.sides.exchange.exchangeserver import ExchangeServer

client_port = random.randint(20000, 25000)
server_port = random.randint(20000, 25000)


def get_crypto_data(values: List[str], k: int) -> CryptoData:
    p = get_p()
    c, d = get_cd(p)
    strings = seed_deck_values(values, p)
    return CryptoData(
        N=len(values),
        k=k,
        strings=strings,
        p=p,
        c=c,
        d=d,
    )


def server_thread():
    server_communicator = StreamCommunicator('localhost', client_port, server_port)
    server = ExchangeServer(server_communicator)
    client_values = server.wait_for_connection_and_crypto_values()
    logging.info(f'Got values from client: {client_values}, is it ok?')
    c, d = get_cd(client_values['p'])
    server.continue_communication(c, d)
    logging.info('Server got deck!')
    server_communicator.stop()


def client_thread():
    values = [str(x) for x in range(100, 150)]
    crypto_data = get_crypto_data(values, 20)
    client_communicator = StreamCommunicator('localhost', server_port, client_port)
    client = ExchangeClient(client_communicator)
    client.trade(crypto_data)
    logging.info('Client got deck!')
    client_communicator.stop()


def main():
    logging.basicConfig(level=logging.INFO)
    Thread(target=client_thread).start()
    Thread(target=server_thread).start()


if __name__ == '__main__':
    main()
