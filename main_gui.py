from tkinter import ttk
import tkinter as tk
from tkinter import filedialog as fd
from main import main


class FrameCreator(ttk.LabelFrame):
    def __init__(self, parent, text, column, row):
        super().__init__(master=parent, text=text, padding=5, height=100)
        self.grid(column=column, row=row, columnspan=1, sticky=tk.NSEW)
        self.labels = []
        self.entries = []
        self.buttons = []

    def add_label(self, text):
        self.labels.append(ttk.Label(text=text, padding=5, master=self, font=("Arial", 12)))
        self.labels[-1].pack(padx=5, pady=5)
        return self

    def add_entry(self, text_variable):
        self.entries.append(ttk.Entry(width=30, textvariable=text_variable, master=self))
        self.entries[-1].pack(padx=5, pady=5)
        return self

    def add_button(self, text, function, style=""):
        self.buttons.append(ttk.Button(width=10, text=text, padding=1, master=self, command=function))
        if style != "":
            self.buttons[-1].config(style=style)
        self.buttons[-1].pack(padx=5, pady=5)
        return self


class MainGui(ttk.Frame):
    def choose_file(self, text):
        text.set(fd.askopenfilename(
            filetypes=[("All Files", "*.*"), ("Text Files", "*.txt")]
        ))

    def __init__(self, parent):
        ttk.Frame.__init__(self)

        self.m = main()

        self.rowconfigure([0, 1], weight=1, minsize=50, uniform='a')
        self.columnconfigure([0, 1], weight=1, minsize=50, uniform='a')

        # setup variables
        self.filename = tk.StringVar()
        self.priv_key_filename = tk.StringVar()
        self.pub_key_filename = tk.StringVar()
        self.file_to_verify = tk.StringVar()
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
                                                                                        self.pub_key_filename.get()),
                                  style='Accent.TButton')
                                  # todo make result visible in the entry
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


root = tk.Tk()
root.tk.call("source", "Azure/azure.tcl")
root.tk.call("set_theme", "dark")
app = MainGui(root)
root.title("BSK project main window - 191005 Marcel Zieliński")
root.configure()
app.pack(fill=tk.BOTH, expand=True)
root.mainloop()
