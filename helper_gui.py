import tkinter as tk
from tkinter.constants import *
from tkinter import filedialog as fd


class LocationChooser:
    location = ""
    location_type = "directory"

    def __init__(self, location_type):
        self.location_type = location_type
        self.window = tk.Tk()
        self.window.title("Choose_location")

        self.window.rowconfigure([0, 1], weight=1, minsize=50)
        self.window.columnconfigure([0, 1], weight=1, minsize=50)

        self.frame1 = tk.Frame(master=self.window, bg='white')
        self.frame1.grid(column=0, row=0, padx=10, pady=10, sticky="ns")

        self.label1 = tk.Label(text="Choose location", master=self.frame1, bg='white', font=("Arial"))
        self.label1.pack(padx=5, pady=5)

        self.ent1 = tk.Entry(fg='green', width=50, master=self.frame1)
        self.ent1.pack()

        self.btn2 = tk.Button(text="Browse", master=self.frame1, bg='yellow', command=lambda: self.open_file())
        self.btn2.pack()

        self.ret_location_button = tk.Button(text="save_location", master=self.frame1,
                                             bg='green', command=lambda: self.save_location())
        self.ret_location_button.pack()

        self.window.mainloop()

    def open_file(self):
        path = ""

        if self.location_type == "file":
            path = fd.askopenfilename(
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
        elif self.location_type == "directory":
            path = fd.askdirectory()

        self.location = path
        self.ent1.delete(0, END)
        self.ent1.insert(0, self.location)

    def save_location(self):
        self.location = self.ent1.get()
        self.window.destroy()


class PinInputter:
    pin = ""

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Enter pin")

        self.window.rowconfigure([0, 1], weight=1, minsize=50)
        self.window.columnconfigure([0, 1], weight=1, minsize=50)

        self.frame1 = tk.Frame(master=self.window, bg='white')
        self.frame1.grid(column=0, row=0, padx=10, pady=10, sticky="ns")

        self.label1 = tk.Label(text="Put in 4 digit pin", master=self.frame1, bg='white', font=("Arial"))
        self.label1.pack(padx=5, pady=5)

        self.ent1 = tk.Entry(fg='green', width=50, master=self.frame1, show="*")
        self.ent1.pack()

        self.ret_location_button = tk.Button(text="save", master=self.frame1,
                                             bg='green', command=lambda: self.save_pin())
        self.ret_location_button.pack()

        self.window.mainloop()

    def save_pin(self):
        self.pin = self.ent1.get()
        self.window.destroy()
