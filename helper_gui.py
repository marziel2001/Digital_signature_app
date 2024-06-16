import tkinter as tk
from tkinter import filedialog as fd
from FrameCreator import FrameCreator


class LocationChooser:
    location_type = "directory"

    def __init__(self, location_type, of_what, update_location):
        self.location_type = location_type
        self.window = tk.Toplevel()
        self.window.title("Choose_location")

        self.window.rowconfigure([0], weight=1, minsize=50)
        self.window.columnconfigure([0], weight=1, minsize=50)

        self.location = tk.StringVar()

        self.frame1 = (FrameCreator(self.window, "Choosing location", 0, 0)
                       .add_label("Choose location of " + of_what)
                       .add_entry(self.location)
                       .add_button("Browse", lambda: self.open_file())
                       .add_button("Confirm", lambda: self.save_location(update_location))
                       )

        self.window.wait_window()

    def save_location(self, update_location):
        update_location(self.location.get())
        self.window.destroy()

    def open_file(self):
        path = ""

        if self.location_type == "file":
            path = fd.askopenfilename(
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
        elif self.location_type == "directory":
            path = fd.askdirectory()

        self.location.set(path)
        self.window.lift()


class PinInputter:

    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Enter pin")

        self.window.rowconfigure([0], weight=1, minsize=50)
        self.window.columnconfigure([0], weight=1, minsize=50)

        self.pin = tk.StringVar()

        self.frame1 = (FrameCreator(self.window, "Choosing pin", 0, 0)
                       .add_label("Enter 4 digit pin")
                       .add_entry(self.pin, show="*")
                       .add_button("Save", lambda: self.save_pin())
                       )

        self.window.wait_window(self.window)

    def save_pin(self):
        self.pin = self.pin.get()
        self.window.destroy()
