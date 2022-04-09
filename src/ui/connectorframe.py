import logging
import tkinter
import tkinter as tk
from tkinter import messagebox

from src.lib.crypto.cryptodata import CryptoData
from src.lib.sides.communication.streamcommunicator import StreamCommunicator
from src.lib.sides.exchange.exchangeclient import ExchangeClient
from src.ui.utils import StringInput, LabeledIntInput


class ConnectorFrame(tk.Frame):
    crypto_data: CryptoData
    ip: str = 'localhost'
    server_port: int = 23001
    client_port: int = 23002

    def __init__(self, crypto_data: CryptoData, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.crypto_data = crypto_data

        row = 0

        def set_ip(v):
            self.ip = v

        tk.Label(self, text='IP').grid(row=row, column=0)
        StringInput(self.ip, on_change=set_ip, master=self).grid(row=row, column=1)

        row += 1

        def set_server_port(v):
            self.server_port = v
        tk.Label(self, text='Server port').grid(row=row, column=0)
        LabeledIntInput(None, self.server_port, from_=1, to=2 ** 16, on_change=set_server_port, master=self).grid(row=row, column=1)

        row += 1

        def set_client_port(v):
            self.client_port = v
        tk.Label(self, text='Client port').grid(row=row, column=0)
        LabeledIntInput(None, self.client_port, from_=1, to=2 ** 16, on_change=set_client_port, master=self).grid(row=row, column=1)

        row += 1

        tk.Button(self, text="Connect", command=self.connect).grid(row=row, column=0, columnspan=2)

    def connect(self):
        client_communicator = None
        try:
            client_communicator = StreamCommunicator(self.ip, self.server_port, self.client_port)
            logging.debug('Created communicator')
            client = ExchangeClient(client_communicator)
            logging.debug('Created exchange client')
            client.trade(self.crypto_data)
            logging.debug('Traded')
            logging.info(f'Client got deck! ({client.get_deck()})')
        except Exception as e:
            logging.error('Error!')
            messagebox.showwarning(title='Error!', message=str(e))
        finally:
            if client_communicator:
                client_communicator.stop()
