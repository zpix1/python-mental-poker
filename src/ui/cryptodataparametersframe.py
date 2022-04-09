import tkinter as tk

from src.lib.crypto.cryptodata import CryptoData
from src.ui.utils import LabeledIntInput


class CryptoDataParametersFrame(tk.Frame):
    def __init__(self, crypto_data: CryptoData, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.config(padx=10)

        tk.Label(self, text="Parameters").grid(row=0, column=0, columnspan=2)

        row = 1

        tk.Label(self, text='p', width=5).grid(row=row, column=0)
        LabeledIntInput(None, crypto_data.p, from_=0, to=None, on_change=None, readonly=True, master=self).grid(row=row,
                                                                                                                column=1)

        row += 1
        tk.Label(self, text='c', width=5).grid(row=row, column=0)
        LabeledIntInput(None, crypto_data.c, from_=0, to=None, on_change=None, readonly=True, master=self).grid(row=row,
                                                                                                                column=1)

        row += 1
        tk.Label(self, text='d', width=5).grid(row=row, column=0)
        LabeledIntInput(None, crypto_data.d, from_=0, to=None, on_change=None, readonly=True, master=self).grid(row=row,
                                                                                                                column=1)

        row += 1

        def set_k(v):
            crypto_data.k = v

        tk.Label(self, text='k', width=5).grid(row=row, column=0)
        LabeledIntInput(None, crypto_data.k, from_=1, to=100, on_change=set_k, master=self).grid(row=row,
                                                                                                  column=1)
