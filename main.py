import rsa
from rsa import VerificationError
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad

import globals
from helper import Helper
import xml.etree.ElementTree as ET
from datetime import datetime
from globals import AES_BLOCK_SIZE

import tkinter as tk

class main():
    def __init__(self):
            self.helper = Helper()

    def get_priv_key(self, filepath):
        with open(filepath, "rb") as f:
            priv_key_2 = f.read()

        priv_key_2_decoded = self.decipher_w_aes(priv_key_2, self.helper.enter_pin())
        privkey2reloaded = rsa.PrivateKey._load_pkcs1_der(priv_key_2_decoded)

        return privkey2reloaded


    def get_pub_key(self, filepath):
        with open(filepath) as f:
            pub_key_2 = f.read()

        pub_key_2_reloaded = rsa.PublicKey.load_pkcs1(pub_key_2.encode('utf8'))
        return pub_key_2_reloaded


    def decipher_w_aes(self, encrypted_content, PIN):
        key = self.helper.hash_pin(PIN)
        iv = encrypted_content[:AES_BLOCK_SIZE]
        encrypted_content = encrypted_content[AES_BLOCK_SIZE:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_content = cipher.decrypt(encrypted_content)
        unpadded_content = unpad(decrypted_content, AES_BLOCK_SIZE)
        return unpadded_content


    def __sign_hash__(self, hash, key):
        signature = rsa.sign_hash(hash, key, 'SHA-256')
        return signature


    def general_purpose_encrypt_rsa(self, filename="test.html"):
        pub_key = self.get_pub_key()

        with open(filename, 'rb') as f:
            fb = f.read()

        encrypted_content = rsa.encrypt(fb, pub_key)

        with open(filename + ".rsa", 'wb') as f:
            f.write(encrypted_content)


    def general_purpose_decrypt_rsa(self, encrypted_content_filename="test.html.rsa"):
        with open(encrypted_content_filename, 'rb') as f:
            fb = f.read()

        priv_key = self.get_priv_key()

        decrypted_content = rsa.decrypt(fb, priv_key)

        with open(encrypted_content_filename.removesuffix('.rsa'), 'wb') as f:
            f.write(decrypted_content)

        return decrypted_content


    def verify_signature(self, file_to_check, signature_file, public_key):
        loaded_pub_key = self.get_pub_key(public_key)
        with open(file_to_check, 'rb') as f:
            original = f.read()

        with open(signature_file, 'rb') as f:
            signature = f.read() # todo: change to separate function that reads signature from xml tag

        try:
            rsa.verify(original, signature, loaded_pub_key)
        except VerificationError:
            print("Plik został zmieniony!")
        else:
            print("Plik jest oryginalny")


    def __hash_file__(self, file):
        with open(file, 'rb') as f:
            fb = f.read()

        _hash = rsa.compute_hash(fb, 'SHA-256')
        return _hash


    def create_xml(self):
        root = ET.Element('signature')

        document = ET.SubElement(root, 'document')
        size = ET.SubElement(document, 'size')
        size.text = 'sizeeeee'

        extension = ET.SubElement(document, 'extension')
        extension.text = 'extensiooooooon'

        date_of_modification = ET.SubElement(document, 'mod-date')
        date_of_modification.text = '1970-01-01'

        user = ET.SubElement(root, 'user')
        name = ET.SubElement(user, 'name')
        name.text = 'imie'

        hash = ET.SubElement(root, 'document-hash')
        hash.text = 'tu bedzie hash'

        time = ET.SubElement(root, 'timestamp')
        time.text = str(datetime.now())

        bxml = ET.tostring(root)


        location = self.helper.choose_directory("for xml")

        with open(location + "test.xml", "wb") as f:
            f.write(bxml)

    def sign_document(self, filename, priv_key_filename):
        loaded_priv_key = self.get_priv_key(priv_key_filename)
        _hash = self.__hash_file__(filename)
        signature = self.__sign_hash__(_hash, loaded_priv_key)

        # todo: pass parameters and fill up the xml corretly
        self.create_xml()

        with open('signature.sha256.rsa', 'wb') as f:
            f.write(signature)

#
# if globals.GUI_MODE == 0:
#     print("Enter mode:\n" +
#           "1. Signing a document\n" +
#           "2. Veryfying signature\n" +
#           "3. Test general purpose encryption \n" +
#           "4. Test general purpose decryption \n" +
#           "5. Generate XML document\n")
#
#     mode = input()
#
#     if mode == '1':
#         filename = input("Enter filename to sign")
#         sign_document(filename)
#
#     if mode == '2':
#         filename = input("Enter filename to verify")
#         verify_signature(filename, "signature.sha256.rsa", get_pub_key())
#
#     if mode == '3':
#         general_purpose_encrypt_rsa()
#
#     if mode == '4':
#         general_purpose_decrypt_rsa()
#
