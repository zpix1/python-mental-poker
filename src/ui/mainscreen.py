import logging
import tkinter as tk

from src.lib.crypto.cryptodata import CryptoData
from src.ui.connectorframe import ConnectorFrame
from src.ui.cryptodataparametersframe import CryptoDataParametersFrame
from src.ui.logframe import LogFrame, LogFrameHandler
from src.ui.cryptodatavaluesframe import CryptoDataValuesFrame


# value         n, k
# value         p
# value         logs
# value
class AppFrame(tk.Frame):
    crypto_data: CryptoData

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.log_frame = LogFrame()
        self.log_frame.grid(row=1, column=1)
        logging.getLogger('').addHandler(LogFrameHandler(self.log_frame))

        self.crypto_data = CryptoData.get_sample_instance()

        self.values_frame = CryptoDataValuesFrame(crypto_data=self.crypto_data)
        self.values_frame.grid(row=0, column=0, sticky=tk.N)

        self.crypto_data_frame = CryptoDataParametersFrame(crypto_data=self.crypto_data)
        self.crypto_data_frame.grid(row=0, column=1, sticky=tk.N)

        self.connector_frame = ConnectorFrame(crypto_data=self.crypto_data)
        self.connector_frame.grid(row=1, column=0, sticky=tk.N)