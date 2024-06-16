from tkinter import ttk
import tkinter as tk

class FrameCreator(ttk.LabelFrame):
    def __init__(self, parent, text, column, row):
        super().__init__(master=parent, text=text)
        self.pack_propagate(True)
        self.configure(width=400)
        self.grid(column=column, row=row, columnspan=1, sticky=tk.NS, padx=15, pady=5, ipadx=15)
        self.labels = []
        self.entries = []
        self.buttons = []

    def add_label(self, text):
        self.labels.append(ttk.Label(text=text, padding=5, master=self, font=("Arial", 12)))
        self.labels[-1].pack(padx=5, pady=5)
        return self

    def add_entry(self, text_variable, disabled=False, show=None):
        self.entries.append(ttk.Entry(width=30, textvariable=text_variable, master=self, font=("Arial", 8)))
        if disabled:
            self.entries[-1].configure(state=tk.DISABLED)
        if show == "*":
            self.entries[-1].configure(show="*")
        self.entries[-1].pack(padx=2, pady=2)
        return self

    def add_button(self, text, function, style=""):
        self.buttons.append(ttk.Button(width=10, text=text, padding=1, master=self, command=function))
        if style != "":
            self.buttons[-1].config(style=style)
        self.buttons[-1].pack(padx=5, pady=5)
        return self
