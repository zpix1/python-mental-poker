from enum import Enum


# types of messages both server and client can send to each other
class ProtocolSteps(Enum):
    ABORT = 'ABORT'
    HELLO = 'HELLO CRYPTO DECK v1.0'
    END = 'END'

    # types of messages client send to server
    CRYPTO_VALUES_AND_DECK = 'CRYPTO VALUES AND DECK'
    SERVER_DECK = 'SERVER DECK'

    # types of messages server send to client
    CLIENT_DECK_AND_DOUBLE_ENCRYPTED_END = 'CLIENT DECK AND DOUBLE ENCRYPTED END'
