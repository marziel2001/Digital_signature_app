import tkinter as tk
from tkinter.constants import *
from tkinter import filedialog as fd
from ttf import generate_and_save_keys

class ttf_gui:
    location = ""

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Generate keys")

        self.window.rowconfigure([0, 1], weight=1, minsize=50)
        self.window.columnconfigure([0, 1], weight=1, minsize=50)

        self.frame1 = tk.Frame(master=self.window, bg='white')
        self.frame1.grid(column=0, row=0, padx=10, pady=10, sticky="ns")

        tk.Button(text="Generate!", master=self.frame1, bg='yellow', command=lambda: self.close()).pack()

        self.window.mainloop()

    def close(self):
        self.window.destroy()
