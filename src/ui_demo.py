import logging
import tkinter as tk

from src.ui.mainscreen import AppFrame

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - [%(levelname)s] -  %(threadName)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )

    window = tk.Tk()
    window.title("Crypto Data Exchange")

    app = AppFrame(window)
    app.grid(row=0, column=0)
    window.resizable(False, False)
    window.mainloop()
