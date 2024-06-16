from tkinter import ttk
import tkinter as tk
from tkinter.ttk import *
from tkinter import filedialog as fd
from main import main


class MainGui(ttk.Frame):
    def choose_file(self, text):
        text.set(fd.askopenfilename(
            filetypes=[("All Files", "*.*"), ("Text Files", "*.txt")]
        ))

    def __init__(self, parent):
        ttk.Frame.__init__(self)

        self.m = main()

        self.rowconfigure([0, 1], weight=1, minsize=50, uniform='a')
        self.columnconfigure([0, 1], weight=1, minsize=50,  uniform='a')

        # setup variables
        self.filename = tk.StringVar()
        self.priv_key_filename = tk.StringVar()
        self.pub_key_filename = tk.StringVar()
        self.file_to_verify = tk.StringVar()
        self.signature_file = tk.StringVar()
        self.file_to_encrypt = tk.StringVar()
        self.file_to_decrypt = tk.StringVar()

        # part 1
        self.SigningFrame = ttk.LabelFrame(master=self, text="Signing", padding=10)
        self.SigningFrame.grid(column=0, columnspan=1, row=0, sticky="nwse")

        self.SignLabel = ttk.Label(text="File location", master=self.SigningFrame, font=("Arial"))
        self.SignLabel.pack(padx=5, pady=5)

        self.choose_file_entry = ttk.Entry(width=50, master=self.SigningFrame, textvariable=self.filename)
        self.choose_file_entry.pack()

        self.choose_file_btn = ttk.Button(text="Choose file", master=self.SigningFrame,command=lambda: self.choose_file(self.filename))
        self.choose_file_btn.pack()

        self.SignPrivKeyLabel = ttk.Label(text="Priv Key location", master=self.SigningFrame, font=("Arial"))
        self.SignPrivKeyLabel.pack(padx=5, pady=5)

        self.choose_key_entry = ttk.Entry(width=50, master=self.SigningFrame, textvariable=self.priv_key_filename)
        self.choose_key_entry.pack()

        self.choose_priv_key_btn = ttk.Button(text="Choose priv key", master=self.SigningFrame, command=lambda: self.choose_file(self.priv_key_filename))
        self.choose_priv_key_btn.pack()

        self.sign_button = ttk.Button(text="Sign", master=self.SigningFrame,
                                     command=lambda: self.m.sign_document(self.filename.get(), self.priv_key_filename.get()))
        self.sign_button.pack()

        # part 2
        self.VerificationFrame = ttk.LabelFrame(master=self, text="Signature Verification")
        self.VerificationFrame.grid(column=0, columnspan=1, row=1, sticky="nwse")

        self.VerificationLabel = ttk.Label(text="File to verify", master=self.VerificationFrame, font=("Arial"))
        self.VerificationLabel.pack(padx=5, pady=5)

        self.verif_file_location = ttk.Entry(width=50, master=self.VerificationFrame, textvariable=self.file_to_verify)
        self.verif_file_location.pack()

        self.verify_browse_button = ttk.Button(text="Browse", master=self.VerificationFrame, command=lambda: self.choose_file(self.file_to_verify))
        self.verify_browse_button.pack()

        self.SignatureLabel = ttk.Label(text="Signature file", master=self.VerificationFrame, font=("Arial"))
        self.SignatureLabel.pack(padx=5, pady=5)

        self.verif_sig_file = ttk.Entry(width=50, master=self.VerificationFrame, textvariable=self.signature_file)
        self.verif_sig_file.pack()

        self.choose_pub_key_btn = ttk.Button(text="Browse", master=self.VerificationFrame, command=lambda: self.choose_file(self.signature_file))
        self.choose_pub_key_btn.pack()

        self.PubKeyLabel = ttk.Label(text="Public key", master=self.VerificationFrame, font=("Arial"))
        self.PubKeyLabel.pack(padx=5, pady=5)

        self.verif_pub_key_entr = ttk.Entry(width=50, master=self.VerificationFrame, textvariable=self.pub_key_filename)
        self.verif_pub_key_entr.pack()

        self.choose_pub_key_btn = ttk.Button(text="Choose pub key", master=self.VerificationFrame, command=lambda: self.choose_file(self.pub_key_filename))
        self.choose_pub_key_btn.pack()

        self.verify_button = ttk.Button(text="Verify", master=self.VerificationFrame, command=lambda: self.m.verify_signature(self.file_to_verify.get(), self.signature_file.get(), self.pub_key_filename.get()))
        self.verify_button.pack()

        # part 3

        self.EncryptionFrame = ttk.LabelFrame(master=self, text="File Encryption")
        self.EncryptionFrame.grid(column=1, columnspan=1, row=0, sticky="nwse")

        self.EncryptionLabel = ttk.Label(text="File to encrypt", master=self.EncryptionFrame, font=("Arial"))
        self.EncryptionLabel.pack(padx=5, pady=5)

        self.file_to_encrypt_entr = ttk.Entry(width=50, master=self.EncryptionFrame, textvariable=self.file_to_encrypt)
        self.file_to_encrypt_entr.pack()

        self.choose_pub_key_btn = ttk.Button(text="Browse", master=self.EncryptionFrame, command=lambda: self.choose_file(self.file_to_encrypt))
        self.choose_pub_key_btn.pack()

        self.PubKeyLabel = ttk.Label(text="Public key", master=self.EncryptionFrame, font=("Arial"))
        self.PubKeyLabel.pack(padx=5, pady=5)

        self.verif_pub_key_entr = ttk.Entry(width=50, master=self.EncryptionFrame, textvariable=self.pub_key_filename)
        self.verif_pub_key_entr.pack()

        self.choose_pub_key_btn = ttk.Button(text="Choose pub key", master=self.EncryptionFrame, command=lambda: self.choose_file(self.pub_key_filename))
        self.choose_pub_key_btn.pack()


        self.encrypt_button = ttk.Button(text="Encrypt", master=self.EncryptionFrame, command=lambda: self.m.general_purpose_encrypt_rsa(self.file_to_encrypt.get(), self.pub_key_filename.get()))
        self.encrypt_button.pack()

        # part 4

        self.DecryptionFrame = ttk.LabelFrame(master=self, text="File Decryption")
        self.DecryptionFrame.grid(column=1, columnspan=1, row=1, sticky="nwse")

        self.DecryptionLabel = ttk.Label(text="File to dencrypt", master=self.DecryptionFrame, font=("Arial"))
        self.DecryptionLabel.pack(padx=5, pady=5)

        self.file_to_decrypt_entr = ttk.Entry(width=50, master=self.DecryptionFrame, textvariable=self.file_to_decrypt)
        self.file_to_decrypt_entr.pack()

        self.choose_pub_key_btn = ttk.Button(text="Browse", master=self.DecryptionFrame, command=lambda: self.choose_file(self.file_to_decrypt))
        self.choose_pub_key_btn.pack()

        self.PrivKeyLabel = ttk.Label(text="Private key", master=self.DecryptionFrame, font=("Arial"))
        self.PrivKeyLabel.pack(padx=5, pady=5)

        self.decr_priv_key_entr = ttk.Entry(width=50, master=self.DecryptionFrame, textvariable=self.priv_key_filename)
        self.decr_priv_key_entr.pack()

        self.choose_decr_priv_key_btn = ttk.Button(text="Choose pub key", master=self.DecryptionFrame,command=lambda: self.choose_file(self.priv_key_filename))
        self.choose_decr_priv_key_btn.pack()

        self.decrypt_button = ttk.Button(text="Decrypt", master=self.DecryptionFrame, command=lambda: self.m.general_purpose_decrypt_rsa(self.file_to_decrypt.get(), self.priv_key_filename.get()))
        self.decrypt_button.pack()




root =  tk.Tk()
# Simply set the theme
root.tk.call("source", "Azure/azure.tcl")
root.tk.call("set_theme", "dark")

app = MainGui(root)
root.title("BSK project main window - 191005 Marcel Zieliński")
root.configure()
app.pack(fill=tk.BOTH, expand=True)
root.mainloop()
