import rsa
from Common.helper_gui import LocationChooser
from Common.helper_gui import PinInputter
import os


class Helper:
    def __init__(self):
        self.location = ""

    def choose_file(self, what):
        return self.__choose__("file", what)

    def choose_directory(self, what):
        return self.__choose__("directory", what)

    def update_location(self, location):
        self.location = location
        print("updated location: " + location)

    def __choose__(self, location_type, what):
        location_selector = LocationChooser(location_type, what, self.update_location)

        #location = location_selector.location.get()

        if self.location == "":
            self.location = self.location + os.getcwd()

        self.location = self.location + "/"
        print("Location from __choose__: " + self.location)
        return self.location

    @staticmethod
    def enter_pin():
        pin = PinInputter().pin
        return pin

    @staticmethod
    def hash_pin(pin):
        return rsa.compute_hash(pin.encode('utf8'), 'SHA-256')
