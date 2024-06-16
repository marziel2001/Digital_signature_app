import tkinter as tk
from tkinter import filedialog as fd
from main import main


class MainGui:
    def choose_file(self, text):
        text.set(fd.askopenfilename(
            filetypes=[("All Files", "*.*"), ("Text Files", "*.txt")]
        ))

        print(self.filename)

    def __init__(self):
        self.m = main()
        self.window = tk.Tk()
        self.window.title("BSK project main window - 191005 Marcel Zieliński")
        self.window.configure(bg="black")

        self.window.rowconfigure([0, 1], weight=1, minsize=50, uniform='a')
        self.window.columnconfigure([0, 1], weight=1, minsize=50,  uniform='a')

        self.filename = tk.StringVar()
        self.priv_key_filename = tk.StringVar()

        self.SigningFrame = tk.LabelFrame(master=self.window, bg='white', text="Signing", padx=10, pady=10)
        self.SigningFrame.grid(column=0, columnspan=1, row=0, padx=10, pady=10, sticky="nwse")

        self.SignLabel = tk.Label(text="File location", master=self.SigningFrame, bg='white', font=("Arial"))
        self.SignLabel.pack(padx=5, pady=5)

        self.choose_file_entry = tk.Entry(width=50, master=self.SigningFrame, textvariable=self.filename)
        self.choose_file_entry.pack()

        self.choose_file_btn = tk.Button(text="Choose file", master=self.SigningFrame,
                                         bg='yellow', command=lambda: self.choose_file(self.filename))
        self.choose_file_btn.pack()

        self.choose_key_entry = tk.Entry(width=50, master=self.SigningFrame, textvariable=self.priv_key_filename)
        self.choose_key_entry.pack()

        self.choose_priv_key_btn = tk.Button(text="Choose priv key", master=self.SigningFrame,
                                         bg='yellow', command=lambda: self.choose_file(self.priv_key_filename))
        self.choose_priv_key_btn.pack()

        self.sign_button = tk.Button(text="Sign", master=self.SigningFrame, bg='yellow',
                                     command=lambda: self.m.sign_document(self.filename.get(), self.priv_key_filename.get()))
        self.sign_button.pack()

        self.window.mainloop()



MainGui()
#
#
# class LocationChooser:
#     location = ""
#     location_type = "directory"
#
#     def __init__(self, location_type, of_what):
#         self.location_type = location_type
#         self.window = tk.Tk()
#         self.window.title("Choose_location")
#
#         self.window.rowconfigure([0, 1], weight=1, minsize=50)
#         self.window.columnconfigure([0, 1], weight=1, minsize=50)
#
#         self.frame1 = tk.Frame(master=self.window, bg='white')
#         self.frame1.grid(column=0, row=0, padx=10, pady=10, sticky="ns")
#
#         self.label1 = tk.Label(text="Choose location of " + of_what, master=self.frame1, bg='white', font=("Arial"))
#         self.label1.pack(padx=5, pady=5)
#
#         self.ent1 = tk.Entry(fg='green', width=50, master=self.frame1)
#         self.ent1.pack()
#
#         self.btn2 = tk.Button(text="Browse", master=self.frame1, bg='yellow', command=lambda: self.open_file())
#         self.btn2.pack()
#
#         self.ret_location_button = tk.Button(text="save_location", master=self.frame1,
#                                              bg='green', command=lambda: self.save_location())
#         self.ret_location_button.pack()
#
#         self.window.mainloop()

