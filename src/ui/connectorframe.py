import logging
import tkinter
import tkinter as tk
from threading import Thread
from tkinter import messagebox

from src.lib.crypto.cryptodata import CryptoData
from src.lib.crypto.utils import get_cd
from src.lib.sides.communication.communicator import Communicator
from src.lib.sides.communication.streamcommunicator import StreamCommunicator
from src.lib.sides.exchange.exchangeclient import ExchangeClient
from src.lib.sides.exchange.exchangeserver import ExchangeServer
from src.ui.utils import StringInput, LabeledIntInput


class ConnectorFrame(tk.Frame):
    crypto_data: CryptoData
    ip: str = 'localhost'
    server_port: int = 23001
    client_port: int = 23002
    communicator: Communicator = None
    listen_thread: Thread = None
    wait_thread: Thread = None

    def __init__(self, crypto_data: CryptoData, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.config(padx=10)

        self.crypto_data = crypto_data

        row = 0

        tk.Label(self, text='Connection').grid(row=row, column=0, columnspan=2)

        row += 1

        def set_ip(v):
            self.ip = v

        tk.Label(self, text='IP').grid(row=row, column=0)
        StringInput(self.ip, on_change=set_ip, master=self).grid(row=row, column=1)

        row += 1

        def set_server_port(v):
            self.server_port = v

        tk.Label(self, text='Server port').grid(row=row, column=0)
        LabeledIntInput(None, self.server_port, from_=1, to=2 ** 16, on_change=set_server_port, master=self).grid(
            row=row, column=1)

        row += 1

        def set_client_port(v):
            self.client_port = v

        tk.Label(self, text='Client port').grid(row=row, column=0)
        LabeledIntInput(None, self.client_port, from_=1, to=2 ** 16, on_change=set_client_port, master=self).grid(
            row=row, column=1)

        row += 1

        self.listen_button = tk.Button(self, text="Start listening", command=self.listen)
        self.listen_button.grid(row=row, column=0, columnspan=2)

        row += 1

        self.connect_button = tk.Button(self, text="Connect", state='disabled', command=self.connect)
        self.connect_button.grid(row=row, column=0, columnspan=2)

        row += 1

        self.wait_button = tk.Button(self, text="Start waiting for connection", state='disabled', command=self.wait_for_connection)
        self.wait_button.grid(row=row, column=0, columnspan=2)

    def listen(self):
        self.listen_thread = Thread(target=self.start_listening, daemon=True)
        self.listen_thread.start()
        self.connect_button.config(state='normal')
        self.wait_button.config(state='normal')
        self.listen_button.config(state='disabled', text='listening...')

    def start_listening(self):
        self.communicator = StreamCommunicator(self.ip, self.server_port, self.client_port)

    def wait_for_connection(self):
        self.connect_button.config(state='disabled')
        self.wait_button.config(state='disabled', text='waiting...')
        self.wait_thread = Thread(target=self.start_waiting_for_connection, daemon=True)
        self.wait_thread.start()

    def start_waiting_for_connection(self):
        while True:
            server = ExchangeServer(self.communicator)
            client_values = server.wait_for_connection_and_crypto_values()
            request = f'A new connection with these parameters:\n' \
                      f'P={client_values["p"]}\n' \
                      f'k={client_values["k"]}\n' \
                      f'Deck: {", ".join(client_values["strings"].keys())}\n' \
                      f'Accept it?'
            if messagebox.askyesno('New connection',request):
                c, d = get_cd(client_values['p'])
                server.continue_communication(c, d)
                messagebox.showinfo('Server got deck!', f'Your secure server deck:\n{", ".join(server.get_deck())}')
            else:
                server.assert_or_abort(False, 'server declined connection')

    def connect(self):
        try:
            logging.debug('Created communicator')
            client = ExchangeClient(self.communicator)
            logging.debug('Created exchange client')
            client.trade(self.crypto_data)
            messagebox.showinfo('Client got deck!', f'Your secure client deck:\n{", ".join(client.get_deck())}')
            logging.debug('Traded')
            logging.info(f'Client got deck! ({client.get_deck()})')
        except Exception as e:
            logging.exception(f'Exchange error {e}')
            messagebox.showwarning('Error!', str(e))
