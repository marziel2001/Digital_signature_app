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
        self.pub_key_filename = tk.StringVar()
        self.file_to_verify = tk.StringVar()
        self.signature_file = tk.StringVar()
        self.file_to_encrypt = tk.StringVar()
        self.file_to_decrypt = tk.StringVar()

        # part 1
        self.SigningFrame = tk.LabelFrame(master=self.window, bg='white', text="Signing", padx=10, pady=10)
        self.SigningFrame.grid(column=0, columnspan=1, row=0, padx=10, pady=10, sticky="nwse")

        self.SignLabel = tk.Label(text="File location", master=self.SigningFrame, bg='white', font=("Arial"))
        self.SignLabel.pack(padx=5, pady=5)

        self.choose_file_entry = tk.Entry(width=50, master=self.SigningFrame, textvariable=self.filename)
        self.choose_file_entry.pack()

        self.choose_file_btn = tk.Button(text="Choose file", master=self.SigningFrame,
                                         bg='yellow', command=lambda: self.choose_file(self.filename))
        self.choose_file_btn.pack()

        self.SignPrivKeyLabel = tk.Label(text="Priv Key location", master=self.SigningFrame, bg='white', font=("Arial"))
        self.SignPrivKeyLabel.pack(padx=5, pady=5)

        self.choose_key_entry = tk.Entry(width=50, master=self.SigningFrame, textvariable=self.priv_key_filename)
        self.choose_key_entry.pack()

        self.choose_priv_key_btn = tk.Button(text="Choose priv key", master=self.SigningFrame,
                                         bg='yellow', command=lambda: self.choose_file(self.priv_key_filename))
        self.choose_priv_key_btn.pack()

        self.sign_button = tk.Button(text="Sign", master=self.SigningFrame, bg='yellow',
                                     command=lambda: self.m.sign_document(self.filename.get(), self.priv_key_filename.get()))
        self.sign_button.pack()

        # part 2
        self.VerificationFrame = tk.LabelFrame(master=self.window, bg='white', text="Signature Verification", padx=10, pady=10)
        self.VerificationFrame.grid(column=0, columnspan=1, row=1, padx=10, pady=10, sticky="nwse")

        self.VerificationLabel = tk.Label(text="File to verify", master=self.VerificationFrame, bg='white', font=("Arial"))
        self.VerificationLabel.pack(padx=5, pady=5)

        self.verif_file_location = tk.Entry(width=50, master=self.VerificationFrame, textvariable=self.file_to_verify)
        self.verif_file_location.pack()

        self.verify_browse_button = tk.Button(text="Browse", master=self.VerificationFrame, bg='yellow', command=lambda: self.choose_file(self.file_to_verify))
        self.verify_browse_button.pack()

        self.SignatureLabel = tk.Label(text="Signature file", master=self.VerificationFrame, bg='white', font=("Arial"))
        self.SignatureLabel.pack(padx=5, pady=5)

        self.verif_sig_file = tk.Entry(width=50, master=self.VerificationFrame, textvariable=self.signature_file)
        self.verif_sig_file.pack()

        self.choose_pub_key_btn = tk.Button(text="Browse", master=self.VerificationFrame,
                                         bg='yellow', command=lambda: self.choose_file(self.signature_file))
        self.choose_pub_key_btn.pack()

        self.PubKeyLabel = tk.Label(text="Public key", master=self.VerificationFrame, bg='white', font=("Arial"))
        self.PubKeyLabel.pack(padx=5, pady=5)

        self.verif_pub_key_entr = tk.Entry(width=50, master=self.VerificationFrame, textvariable=self.pub_key_filename)
        self.verif_pub_key_entr.pack()

        self.choose_pub_key_btn = tk.Button(text="Choose pub key", master=self.VerificationFrame,
                                         bg='yellow', command=lambda: self.choose_file(self.pub_key_filename))
        self.choose_pub_key_btn.pack()

        self.verify_button = tk.Button(text="Verify", master=self.VerificationFrame, bg='yellow', command=lambda: self.m.verify_signature(self.file_to_verify.get(), self.signature_file.get(), self.pub_key_filename.get()))
        self.verify_button.pack()

        # part 3

        self.EncryptionFrame = tk.LabelFrame(master=self.window, bg='white', text="File Encryption", padx=10, pady=10)
        self.EncryptionFrame.grid(column=1, columnspan=1, row=0, padx=10, pady=10, sticky="nwse")

        self.EncryptionLabel = tk.Label(text="File to encrypt", master=self.EncryptionFrame, bg='white', font=("Arial"))
        self.EncryptionLabel.pack(padx=5, pady=5)

        self.file_to_encrypt_entr = tk.Entry(width=50, master=self.EncryptionFrame, textvariable=self.file_to_encrypt)
        self.file_to_encrypt_entr.pack()

        self.choose_pub_key_btn = tk.Button(text="Browse", master=self.EncryptionFrame,
                                         bg='yellow', command=lambda: self.choose_file(self.file_to_encrypt))
        self.choose_pub_key_btn.pack()

        self.PubKeyLabel = tk.Label(text="Public key", master=self.EncryptionFrame, bg='white', font=("Arial"))
        self.PubKeyLabel.pack(padx=5, pady=5)

        self.verif_pub_key_entr = tk.Entry(width=50, master=self.EncryptionFrame, textvariable=self.pub_key_filename)
        self.verif_pub_key_entr.pack()

        self.choose_pub_key_btn = tk.Button(text="Choose pub key", master=self.EncryptionFrame,
                                            bg='yellow', command=lambda: self.choose_file(self.pub_key_filename))
        self.choose_pub_key_btn.pack()


        self.encrypt_button = tk.Button(text="Encrypt", master=self.EncryptionFrame, bg='yellow', command=lambda: self.m.general_purpose_encrypt_rsa(self.file_to_encrypt.get(), self.pub_key_filename.get()))
        self.encrypt_button.pack()

        # part 4

        self.DecryptionFrame = tk.LabelFrame(master=self.window, bg='white', text="File Decryption", padx=10, pady=10)
        self.DecryptionFrame.grid(column=1, columnspan=1, row=1, padx=10, pady=10, sticky="nwse")

        self.DecryptionLabel = tk.Label(text="File to dencrypt", master=self.DecryptionFrame, bg='white', font=("Arial"))
        self.DecryptionLabel.pack(padx=5, pady=5)

        self.file_to_decrypt_entr = tk.Entry(width=50, master=self.DecryptionFrame, textvariable=self.file_to_decrypt)
        self.file_to_decrypt_entr.pack()

        self.choose_pub_key_btn = tk.Button(text="Browse", master=self.DecryptionFrame,
                                         bg='yellow', command=lambda: self.choose_file(self.file_to_decrypt))
        self.choose_pub_key_btn.pack()

        self.PrivKeyLabel = tk.Label(text="Private key", master=self.DecryptionFrame, bg='white', font=("Arial"))
        self.PrivKeyLabel.pack(padx=5, pady=5)

        self.decr_priv_key_entr = tk.Entry(width=50, master=self.DecryptionFrame, textvariable=self.priv_key_filename)
        self.decr_priv_key_entr.pack()

        self.choose_decr_priv_key_btn = tk.Button(text="Choose pub key", master=self.DecryptionFrame,
                                            bg='yellow', command=lambda: self.choose_file(self.priv_key_filename))
        self.choose_decr_priv_key_btn.pack()


        self.decrypt_button = tk.Button(text="Decrypt", master=self.DecryptionFrame, bg='yellow', command=lambda: self.m.general_purpose_decrypt_rsa(self.file_to_decrypt.get(), self.priv_key_filename.get()))
        self.decrypt_button.pack()


        self.window.mainloop()



MainGui()