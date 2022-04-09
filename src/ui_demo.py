import tkinter as tk

from src.ui.mainscreen import AppFrame

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Crypto Data Exchange")

    app = AppFrame(window)
    app.grid(row=0, column=0)
    window.resizable(False, False)
    window.mainloop()
