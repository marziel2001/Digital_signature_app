import rsa
import helper_gui
import globals


def choose_file():
    return __choose__("file")


def choose_directory():
    return __choose__("directory")


def __choose__(location_type):
    location = ""

    if globals.GUI_MODE == 0:
        print("Please provide the drive letter or leave empty for current location")
        location = input()
        if location != "":
            location += ":/"
    else:
        location_selector = helper_gui.LocationChooser(location_type)
        location = location_selector.location

    location = location+"/"

    print("Location: " + location)

    return location


def enter_pin():
    pin = ""

    if globals.GUI_MODE == 0:
        print("Please enter your 4 digit PIN")
        pin = input()
    else:
        pin = helper_gui.PinInputter().pin

    return pin


def hash_pin(pin):
    return rsa.compute_hash(pin.encode('utf8'), 'SHA-256')
