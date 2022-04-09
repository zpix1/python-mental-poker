import tkinter as tk
from typing import Callable, Optional


class LabeledIntInput(tk.Frame):
    def __init__(self, label_str: Optional[str], default_value: int, on_change: Optional[Callable[[int], None]],
                 from_: Optional[int], to: Optional[int], readonly: bool = False, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        if label_str:
            tk.Label(self, text=label_str).grid(row=0, column=0)

        current_value = tk.StringVar(value=str(default_value))

        def on_change_handler():
            value = int(self.spinbox.get())
            on_change(value)

        self.spinbox = tk.Spinbox(self, from_=from_, to=to, textvariable=current_value,
                                  command=on_change_handler)
        self.spinbox.grid(row=0, column=1)
        if readonly:
            self.spinbox.config(state='disabled')


class StringInput(tk.Frame):
    def __init__(self, default_value: str, on_change: Optional[Callable[[str], None]], *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        current_value = tk.StringVar(value=str(default_value))

        def on_change_handler(cv):
            value = cv.get()
            if on_change:
                on_change(value)

        current_value.trace("w", lambda name, index, mode, sv=current_value: on_change_handler(current_value))

        self.spinbox = tk.Entry(self, textvariable=current_value)
        self.spinbox.grid(row=0, column=1)
