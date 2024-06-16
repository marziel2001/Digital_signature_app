from tkinter import ttk
import tkinter as tk
from tkinter import filedialog as fd
from main import Main
from Common.FrameCreator import FrameCreator


class MainGui(ttk.Frame):
    def choose_file(self, text):
        text.set(fd.askopenfilename(
            filetypes=[("All Files", "*.*"), ("Text Files", "*.txt")]
        ))

    def __init__(self, parent):
        ttk.Frame.__init__(self)
        self.rowconfigure([0], weight=1, minsize=50, uniform='a')
        self.rowconfigure([1], weight=1, minsize=50, uniform='b')

        self.columnconfigure([0, 1], weight=1, minsize=50, uniform='a')
        self.columnconfigure([0, 1], weight=1, minsize=50, uniform='a')

        self.configure()
        self.m = Main()

        # setup variables
        self.filename = tk.StringVar()
        self.priv_key_filename = tk.StringVar()
        self.pub_key_filename = tk.StringVar()
        self.file_to_verify = tk.StringVar()
        self.verify_status = tk.StringVar()
        self.signature_file = tk.StringVar()
        self.file_to_encrypt = tk.StringVar()
        self.file_to_decrypt = tk.StringVar()

        # part 1
        self.SigningFrame = (FrameCreator(self, "Signing", 0, 0)
                             .add_label("File location")
                             .add_entry(self.filename)
                             .add_button("Browse", lambda: self.choose_file(self.filename))
                             .add_label("Priv Key location")
                             .add_entry(self.priv_key_filename)
                             .add_button("Browse", lambda: self.choose_file(self.priv_key_filename))
                             .add_button("Sign", lambda: self.m.sign_document(self.filename.get(),
                                                                              self.priv_key_filename.get()),
                                         style='Accent.TButton'))

        # part 2
        self.VerificationFrame = (FrameCreator(self, "Signature Verification", 0, 1)
                                  .add_label("File to verify")
                                  .add_entry(self.file_to_verify)
                                  .add_button("Browse", lambda: self.choose_file(self.file_to_verify))
                                  .add_label("Signature file")
                                  .add_entry(self.signature_file)
                                  .add_button("Browse", lambda: self.choose_file(self.signature_file))
                                  .add_label("Public key")
                                  .add_entry(self.pub_key_filename)
                                  .add_button("Browse", lambda: self.choose_file(self.pub_key_filename))
                                  .add_button("Verify", lambda: self.m.verify_signature(self.file_to_verify.get(),
                                                                                        self.signature_file.get(),
                                                                                        self.pub_key_filename.get(),
                                                                                        self.verify_status),
                                              style='Accent.TButton')
                                  .add_entry(self.verify_status, disabled=True)
                                  )

        # part 3
        self.EncryptionFrame = (FrameCreator(self, "File Encryption", 1, 0)
                                .add_label("File to encrypt")
                                .add_entry(self.file_to_encrypt)
                                .add_button("Browse", lambda: self.choose_file(self.file_to_encrypt))
                                .add_label("Public key")
                                .add_entry(self.pub_key_filename)
                                .add_button("Browse", lambda: self.choose_file(self.pub_key_filename))
                                .add_button("Encrypt",
                                            lambda: self.m.general_purpose_encrypt_rsa(self.file_to_encrypt.get(),
                                                                                       self.pub_key_filename.get()),
                                            style='Accent.TButton')
                                )
        # part 4
        self.DecryptionFrame = (FrameCreator(self, "File Decryption", 1, 1)
                                .add_label("File to decrypt")
                                .add_entry(self.file_to_decrypt)
                                .add_button("Browse", lambda: self.choose_file(self.file_to_decrypt))
                                .add_label("Private key")
                                .add_entry(self.priv_key_filename)
                                .add_button("Browse", lambda: self.choose_file(self.priv_key_filename))
                                .add_button("Decrypt",
                                            lambda: self.m.general_purpose_decrypt_rsa(self.file_to_decrypt.get(),
                                                                                       self.priv_key_filename.get()),
                                            style='Accent.TButton')
                                )


if __name__ == "__main__":
    root = tk.Tk()
    root.tk.call("source", "Azure/azure.tcl")
    root.tk.call("set_theme", "dark")

    app = MainGui(root)

    root.title("BSK project - 191005 Marcel Zieliński")
    root.configure(width=1200, height=900)

    root.pack_propagate(False)
    app.pack(expand=True, fill=tk.Y)

    root.mainloop()

