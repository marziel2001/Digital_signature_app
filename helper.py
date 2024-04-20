import rsa


def choose_drive():
    print("Please provide the drive letter")
    drive = input()

    if drive != "":
        drive += ":/"

    return drive


def enter_pin():
    print("Please enter your 4 digit PIN")
    pin = input()
    return pin


def hash_pin(pin):
    return rsa.compute_hash(pin.encode('utf8'), 'SHA-256')
