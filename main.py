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


def get_priv_key(filename='priv.pem.aes'):
    drive = choose_drive()

    fn = filename

    with open(drive + fn, "rb") as f:
        priv_key_2 = f.read()

    priv_key_2_decoded = decipher_w_aes(priv_key_2, enter_pin())
    privkey2reloaded = rsa.PrivateKey._load_pkcs1_der(priv_key_2_decoded)

    return privkey2reloaded


def get_pub_key(filename='pub.pem'):
    drive = choose_drive()
    fn = filename

    with open(drive + fn) as f:
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


def __sign_hash__(hash, key):
    signature = rsa.sign_hash(hash, key, 'SHA-256')
    return signature


def general_purpose_encrypt_rsa(filename="test.html"):
    pub_key = get_pub_key()

    with open(filename, 'rb') as f:
        fb = f.read()

    encrypted_content = rsa.encrypt(fb, pub_key)

    with open(filename + ".rsa", 'wb') as f:
        f.write(encrypted_content)


def general_purpose_decrypt_rsa(encrypted_content_filename="test.html.rsa"):
    with open(encrypted_content_filename, 'rb') as f:
        fb = f.read()

    priv_key = get_priv_key()

    decrypted_content = rsa.decrypt(fb, priv_key)

    with open(encrypted_content_filename.removesuffix('.rsa'), 'wb') as f:
        f.write(decrypted_content)

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


def __hash_file__(file):
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
    loaded_priv_key = get_priv_key()
    _hash = __hash_file__(filename)
    signature = __sign_hash__(_hash, loaded_priv_key)

    create_xml() # todo: pass parameters and fill up the xml corretly

    with open('signature.sha256.rsa', 'wb') as f:
        f.write(signature)



print("Enter mode:\n" +
      "1. Signing a document\n" +
      "2. Veryfying signature\n" +
      "3. Test general purpose encryption \n" +
      "4. Test general purpose decryption \n" +
      "5. Generate XML document\n")

mode = input()

if mode == '1':
    filename = input("Enter filename to sign")
    sign_document(filename)

if mode == '2':
    filename = input("Enter filename to verify")
    verify_signature(filename, "signature.sha256.rsa", get_pub_key())

if mode == '3':
    general_purpose_encrypt_rsa()

if mode == '4':
    general_purpose_decrypt_rsa()

if mode == '5':
    create_xml()
