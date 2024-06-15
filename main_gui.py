import tkinter as tk
from tkinter.constants import *
from tkinter import filedialog as fd


class MainGui:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("BSK project main window - 191005 Marcel Zieliński")
        self.window.configure(bg="black")

        self.window.rowconfigure([0, 1], weight=1, minsize=50, uniform='a')
        self.window.columnconfigure([0, 1], weight=1, minsize=50,  uniform='a')

        self.SigningFrame = tk.LabelFrame(master=self.window, bg='white', text="Signing", padx=10, pady=10)
        self.SigningFrame.grid(column=0, columnspan=1, row=0, padx=10, pady=10, sticky="nwse")

        self.SignLabel = tk.Label(text="Signing documents", master=self.SigningFrame, bg='white', font=("Arial"))
        self.SignLabel.pack(padx=5, pady=5)

        self.sign_button = tk.Button(text="Sign", master=self.SigningFrame, bg='yellow', command=lambda: print("sign"))
        self.sign_button.pack()



        self.VerificationFrame = tk.LabelFrame(master=self.window, bg='white', text="Verification", padx=10, pady=10)
        self.VerificationFrame.grid(column=0, columnspan=1, row=1, padx=10, pady=10, sticky="nwse")

        self.VerificationLabel = tk.Label(text="Signature Verification", master=self.VerificationFrame, bg='white', font=("Arial"))
        self.VerificationLabel.pack(padx=5, pady=5)

        self.verify_button = tk.Button(text="Verify", master=self.VerificationFrame, bg='yellow', command=lambda: print("verify"))
        self.verify_button.pack()



        self.EncryptionFrame = tk.LabelFrame(master=self.window, bg='white', text="Encryption", padx=10, pady=10)
        self.EncryptionFrame.grid(column=1, columnspan=1, row=1, padx=10, pady=10, sticky="nwse")

        self.EncryptionLabel = tk.Label(text="File encryption", master=self.EncryptionFrame, bg='white', font=("Arial"))
        self.EncryptionLabel.pack(padx=5, pady=5)

        self.encrypt_button = tk.Button(text="Encrypt", master=self.EncryptionFrame, bg='yellow', command=lambda: print("encrypt"))
        self.encrypt_button.pack()


        self.DecryptionFrame = tk.LabelFrame(master=self.window, bg='white', text="Decryption", padx=10, pady=10)
        self.DecryptionFrame.grid(column=1, columnspan=1, row=0, padx=10, pady=10, sticky="nwse")

        self.DecryptionLabel = tk.Label(text="File decryption", master=self.DecryptionFrame, bg='white', font=("Arial"))
        self.DecryptionLabel.pack(padx=5, pady=5)

        self.decrypt_button = tk.Button(text="Decrypt", master=self.DecryptionFrame, bg='yellow', command=lambda: print("decrypt"))
        self.decrypt_button.pack()




        # self.ent1 = tk.Entry(fg='green', width=50, master=self.frame1)
        # self.ent1.pack()

        self.window.mainloop()

