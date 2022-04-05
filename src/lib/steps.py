from enum import Enum


# types of messages both server and client can send to each other
class ProtocolSteps(Enum):
    ABORT = 'ABORT'
    HELLO = 'HELLO CRYPTO DECK v1.0'


# types of messages client send to server
class ClientProtocolSteps(ProtocolSteps):
    DECK = 'DECK'
    CRYPTO_VALUES = 'CRYPTO VALUES'
    DECK_VALUES = 'DECK VALUES'
    SERVER_DECK = 'SERVER DECK'


# types of messages server send to client
class ServerProtocolSteps(ProtocolSteps):
    CLIENT_DECK = 'CLIENT DECK'
    DECK_END = 'DECK END'
