import _queue
import logging
import queue
import socket
from queue import Queue
from threading import Thread

from src.lib.sides.communication.communicator import Communicator


class StreamCommunicator(Communicator):
    timeout = 0.1

    host: str
    listen_port: int
    send_port: int

    stop_flag: bool = False

    receive_queue: 'Queue[bytes]'
    receiver_thread: Thread = None

    sender_queue: 'Queue[bytes]'
    sender_thread: Thread = None

    def __init__(self, host: str, listen_port: int = 23001, send_port: int = 23002):
        self.host = host
        self.listen_port = listen_port
        self.send_port = send_port

        self.receive_queue = Queue()
        self.receiver_thread = Thread(target=self.start_receiver)
        self.receiver_thread.start()

        self.sender_queue = Queue()

        logging.info(f'Starting a new client-server connection listen on {listen_port}, send to {send_port}')

    def send_bytes(self, message: bytes) -> None:
        if not self.sender_thread:
            self.sender_thread = Thread(target=self.start_sender)
            self.sender_thread.start()
        self.sender_queue.put(message)

    def receive_bytes(self) -> bytes:
        while True and not self.stop_flag:
            try:
                return self.receive_queue.get(timeout=self.timeout)
            except _queue.Empty:
                continue
        raise InterruptedError('thread stopped')

    def start_receiver(self) -> None:
        try:
            sock = socket.socket()
            sock.bind(('0.0.0.0', self.listen_port))

            sock.listen(1)
            sock.settimeout(self.timeout)

            while True and not self.stop_flag:
                try:
                    connection, address = sock.accept()
                except TimeoutError:
                    continue
                logging.debug(f'Got a new connection from {address}')
                while True and not self.stop_flag:
                    message_len = int.from_bytes(connection.recv(4), byteorder='big')
                    message_bytes = connection.recv(message_len)
                    self.receive_queue.put(message_bytes)
                connection.close()
        except Exception as e:
            logging.error(e)
            self.stop_flag = True

    def start_sender(self) -> None:
        try:
            sock = socket.socket()
            sock.connect((self.host, self.send_port))
            while True and not self.stop_flag:
                try:
                    msg = self.sender_queue.get(timeout=self.timeout)
                except queue.Empty:
                    continue
                sock.send(len(msg).to_bytes(byteorder='big', length=4))
                sock.send(msg)
            sock.close()
        except Exception as e:
            logging.error(e)
            self.stop_flag = True

    def stop(self):
        self.stop_flag = True
        self.sender_thread.join()
        self.receiver_thread.join()
