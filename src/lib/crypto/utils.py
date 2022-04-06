from typing import List, Dict

from Crypto.Util.number import getPrime
from Crypto.Util.number import getRandomRange, inverse

from src.lib.crypto.cryptodata import CryptoData


def encrypt(crypto_data: CryptoData, value: int) -> int:
    return pow(value, crypto_data.c, crypto_data.p)


def decrypt(crypto_data: CryptoData, value: int) -> int:
    return pow(value, crypto_data.d, crypto_data.p)


def get_p() -> int:
    return getPrime(10)


def get_cd(p: int) -> (int, int):
    c = getRandomRange(1, p - 1)
    d = inverse(c, p - 1)
    return c, d


def seed_deck_values(values: List[str], p: int) -> Dict[str, int]:
    return {
        v: getRandomRange(1, p) for v in values
    }
