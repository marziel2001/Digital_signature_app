import rsa
import globals
import helper_gui
import os


class Helper():
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
        if globals.GUI_MODE == 0:
            print("Please provide the drive letter or leave empty for current location")
            location = input()
            if location != "":
                location += ":/"
        else:
            location_selector = helper_gui.LocationChooser(location_type, what, self.update_location)

            #location = location_selector.location.get()

            if self.location == "":
                self.location = self.location + os.getcwd()

        self.location = self.location + "/"
        print("Location from __choose__: " + self.location)
        return self.location


    def enter_pin(self):
        pin = ""

        if globals.GUI_MODE == 0:
            print("Please enter your 4 digit PIN")
            pin = input()
        else:
            pin = helper_gui.PinInputter().pin

        return pin


    def hash_pin(self, pin):
        return rsa.compute_hash(pin.encode('utf8'), 'SHA-256')
