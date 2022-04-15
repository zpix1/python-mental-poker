import logging
import tkinter as tk
from logging import StreamHandler, LogRecord
from queue import Queue
from threading import Thread


class LogFrameHandler(StreamHandler):
    def __init__(self, log_frame: 'LogFrame'):
        StreamHandler.__init__(self)
        self.log_frame = log_frame
        self.queue = Queue()
        t = Thread(target=self.start_posting, daemon=True)
        t.start()

    def emit(self, record: LogRecord) -> None:
        msg = self.format(record)
        self.queue.put_nowait(msg)

    def start_posting(self):
        while True:
            msg = self.queue.get()
            self.log_frame.log_accept(msg)


class LogFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        tk.Label(self, text="Log").grid(row=0, column=0)
        self.log = tk.Text(self, width=40)
        self.log.grid(row=1, column=0)

    def log_accept(self, msg: str):
        self.log.insert(tk.INSERT, msg + '\n')
