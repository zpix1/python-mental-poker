from dataclasses import dataclass
from typing import Dict
from Crypto.Util.number import isPrime

from src.lib.crypto.cryptoexception import CryptoException


@dataclass
class CryptoData:
    N: int
    k: int
    strings: Dict[str, int]

    p: int
    c: int
    d: int

    def validate(self) -> None:
        if self.N < 3:
            raise CryptoException("N can't be lower than 3")
        if self.k * 2 > self.N:
            raise CryptoException("2*k can't be greater than N")
        if len(self.strings.keys()) != self.N:
            raise CryptoException("Strings key count must be equal to N")
        if not isPrime(self.p):
            raise CryptoException("p is not prime")
        if not pow(self.c * self.d, self.p - 1) == 1:
            raise CryptoException("c*d mod p is not equal to 1")
