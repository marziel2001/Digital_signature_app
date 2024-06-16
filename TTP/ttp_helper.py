import rsa
import globals
import ttp_helper_gui
import os


class Helper():



    def choose_file(self, what):
        return self.__choose__("file", what)


    def choose_directory(self, what):
        return self.__choose__("directory", what)


    def __choose__(self, location_type, what):
        if globals.GUI_MODE == 0:
            print("Please provide the drive letter or leave empty for current location")
            location = input()
            if location != "":
                location += ":/"
        else:
            location_selector = ttp_helper_gui.LocationChooser(location_type, what)
            location = location_selector.location
            if location == "":
                location = location + os.getcwd()

        location = location+"/"
        print("Location from __choose__: " + location)
        return location


    def enter_pin(self):
        pin = ""

        if globals.GUI_MODE == 0:
            print("Please enter your 4 digit PIN")
            pin = input()
        else:
            pin = ttp_helper_gui.PinInputter().pin

        return pin


    def hash_pin(self, pin):
        return rsa.compute_hash(pin.encode('utf8'), 'SHA-256')
