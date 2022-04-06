from abc import ABC, abstractmethod


class Communicator(ABC):
    @abstractmethod
    def send_bytes(self, message: bytes) -> None:
        pass

    @abstractmethod
    def receive_bytes(self) -> bytes:
        pass

    def stop(self):
        pass
