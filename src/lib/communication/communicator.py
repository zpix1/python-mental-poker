from abc import ABC, abstractmethod


class Communicator(ABC):
    @abstractmethod
    def send_string(self):
        pass

    @abstractmethod
    def receive_string(self):
        pass
