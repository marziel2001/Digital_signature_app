import rsa
from rsa import VerificationError
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
from helper import hash_pin
from helper import choose_drive
from helper import enter_pin
import xml.etree.ElementTree as ET
from datetime import datetime
from globals import AES_BLOCK_SIZE


def load_private_key():
    drive = choose_drive()

    with open(drive + 'priv.pem.aes', "rb") as f:
        priv_key_2 = f.read()

    priv_key_2_decoded = decipher_w_aes(priv_key_2, enter_pin())
    privkey2reloaded = rsa.PrivateKey._load_pkcs1_der(priv_key_2_decoded)

    return privkey2reloaded


def load_public_key():
    drive = choose_drive()

    with open(drive + 'pub.pem') as f:
        pub_key_2 = f.read()

    pub_key_2_reloaded = rsa.PublicKey.load_pkcs1(pub_key_2.encode('utf8'))
    return pub_key_2_reloaded


def decipher_w_aes(encrypted_content, PIN):
    key = hash_pin(PIN)
    iv = encrypted_content[:AES_BLOCK_SIZE]
    encrypted_content = encrypted_content[AES_BLOCK_SIZE:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_content = cipher.decrypt(encrypted_content)
    unpadded_content = unpad(decrypted_content, AES_BLOCK_SIZE)
    return unpadded_content


def sign_hash(hash, key):
    signature = rsa.sign_hash(hash, key, 'SHA-256')
    return signature


def general_purpose_encrypt_rsa(content, public_key):
    signature = rsa.encrypt(content, public_key)

    with open('signature.sha256.rsa', 'wb') as f:
        f.write(signature)

    return signature


def general_purpose_decrypt_rsa(encrypted_content, private_key):
    with open(encrypted_content, 'rb') as f:
        fb = f.read()

    decrypted_content = rsa.decrypt(fb, private_key)
    return decrypted_content


def verify_signature(file_to_check, signature_file, public_key):
    with open(file_to_check, 'rb') as f:
        original = f.read()

    with open(signature_file, 'rb') as f:
        signature = f.read() # todo: change to separate function that reads signature from xml tag

    try:
        rsa.verify(original, signature, public_key)
    except VerificationError:
        print("Plik został zmieniony!")
    else:
        print("Plik jest oryginalny")


def hash_file(file):
    with open(file, 'rb') as f:
        fb = f.read()

    _hash = rsa.compute_hash(fb, 'SHA-256')
    return _hash


def create_xml():
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

    drive = choose_drive()

    with open(drive + "test.xml", "wb") as f:
        f.write(bxml)


def sign_document(filename):
    loaded_priv_key = load_private_key()
    _hash = hash_file(filename)
    signature = sign_hash(_hash, loaded_priv_key)

    create_xml() # todo: pass parameters and fill up the xml corretly

    with open('signature.sha256.rsa', 'wb') as f:
        f.write(signature)



print("Enter mode:\n" +
      "1. Signing a document\n" +
      "2. Veryfying signature\n" +
      "3. Test general purpose encryption & decryption\n" +
      "4. Generate XML document\n")

mode = input()

if mode == '1':
    filename = input("Enter filename to sign")
    sign_document(filename)

if mode == '2':
    filename = input("Enter filename to verify")
    verify_signature(filename, "signature.sha256.rsa", load_public_key())

if mode == '3':
    file = "test.html"

    with open(file, 'rb') as f:
        fb = f.read()

    pub_key = load_public_key()

    encrypted_content = general_purpose_encrypt_rsa(fb, pub_key)

    with open(file + ".rsa", 'wb') as f:
        f.write(encrypted_content)

    with open(file + ".rsa", 'rb') as f:
        fb2 = f.read()

    priv_key = load_private_key()
    decrypted_content = general_purpose_decrypt_rsa(fb2, priv_key)

    with open(file + "decrypted.html", 'wb') as f:
        f.write(decrypted_content)

if mode == '4':
    create_xml()
