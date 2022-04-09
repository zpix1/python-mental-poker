import tkinter as tk
from typing import List

from src.lib.crypto.cryptodata import CryptoData
from src.lib.crypto.utils import seed_deck_values
from src.ui.utils import StringInput, LabeledIntInput


class CryptoDataValuesFrame(tk.Frame):
    values: List[str]
    crypto_data: CryptoData

    def __init__(self, crypto_data: CryptoData, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.config(padx=10)

        self.crypto_data = crypto_data
        self.values = list(crypto_data.strings.keys())

        self.rebuild()

    def rebuild(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Values").grid(row=0, column=0, columnspan=2)

        for i, v in enumerate(self.values):
            def on_change(value):
                self.values[i] = value
                self.sync()

            StringInput(v, on_change=on_change, master=self).grid(row=i + 1, column=0, columnspan=2)

        tk.Button(self, text='+', command=self.add_entry).grid(row=len(self.values) + 1, column=0)
        tk.Button(self, text='-', command=self.remove_entry).grid(row=len(self.values) + 1, column=1)

    def sync(self):
        self.rebuild()
        self.crypto_data.N = len(self.values)
        self.crypto_data.strings = seed_deck_values(self.values, self.crypto_data.p)

    def add_entry(self):
        self.values.append(f'Card {len(self.values) + 1}')
        self.sync()

    def remove_entry(self):
        if len(self.values) > 3:
            self.values.pop()
            self.sync()
