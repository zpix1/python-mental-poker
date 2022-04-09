import tkinter as tk


class LogFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        tk.Label(self, text="Log").grid(row=0, column=0)
        self.log = tk.Text(self, width=20)
        self.log.insert(tk.INSERT, '123\n'*100)
        self.log.config(state='disabled')
        self.log.grid(row=1, column=0)
