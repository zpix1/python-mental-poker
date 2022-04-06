import socket

from src.lib.sides.communication.communicator import Communicator


class StreamCommunicator(Communicator):
    host: str
    listen_port: int
    send_port: int

    def __init__(self, host: str, listen_port: int = 23001, send_port: int = 23002):
       self.host = host
       self.listen_port = listen_port
       self.send_port = send_port

    def start_listener(self):
        s = socket.socket()
        s.bind(('0.0.0.0', self.listen_port))

        s.listen(1)
        c, addr = s.accept()
        c.recv(1024)
        c.close()