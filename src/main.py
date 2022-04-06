import logging
from typing import List

from src.lib.crypto.cryptodata import CryptoData
from src.lib.crypto.utils import get_p, get_cd, seed_deck_values
from src.lib.sides.communication.fakecommunicator import FakeCommunicator
from src.lib.sides.exchangeclient import ExchangeClient


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


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    values = [
        'Red',
        'Green',
        'Blue'
    ]

    crypto_data = get_crypto_data(values, 1)

    communicator = FakeCommunicator()
    client = ExchangeClient(communicator)

    client.trade(crypto_data)
