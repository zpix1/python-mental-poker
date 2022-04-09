from math import gcd
from typing import List, Dict

from Crypto.Util.number import getPrime
from Crypto.Util.number import getRandomRange, inverse


def get_p() -> int:
    return getPrime(512)


def get_cd(p: int) -> (int, int):
    c = getRandomRange(1, p - 1)
    if gcd(c, p - 1) != 1:
        return get_cd(p)
    d = inverse(c, p - 1)
    return c, d


def seed_deck_values(values: List[str], p: int) -> Dict[str, int]:
    return {
        v: getRandomRange(2, p - 2) for v in values
    }
