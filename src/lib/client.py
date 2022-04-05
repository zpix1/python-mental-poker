from src.lib.communication.communicator import Communicator
from src.lib.crypto.cryptodata import CryptoData


class ExchangeClient:
    communicator: Communicator
    crypto_data: CryptoData

    def __init__(self, communicator: Communicator, crypto_data: CryptoData):
        self.communicator = communicator
        self.crypto_data = crypto_data
