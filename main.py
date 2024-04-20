import rsa
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes

from rsa import VerificationError

SHA_BLOCK_SIZE = 65536
RSA_KEY_SIZE = 2048


def choose_drive():
    print("please provide the drive letter")
    drive = input()

    if drive != "":
        drive += "/"

    return drive


def enter_PIN():
    print("Please enter your 4 digit PIN")
    PIN = input()
    return PIN


def gen_and_save_keys():
    drive = choose_drive()

    # todo use 4096 in the final version
    (pub_key, priv_key) = rsa.newkeys(RSA_KEY_SIZE)

    with open(drive + 'pub.pem', 'w') as f:
        f.write(pub_key.save_pkcs1().decode('utf8'))

    encrypted_key = cipher_w_aes(priv_key.save_pkcs1('DER'), enter_PIN())

    with open(drive + 'priv.pem.aes', 'wb') as f:
        f.write(encrypted_key)


def load_private_key():
    drive = choose_drive()

    with open(drive + 'priv.pem.aes', "rb") as f:
        priv_key_2 = f.read()

    priv_key_2_decoded = decipher_w_aes(priv_key_2, enter_PIN())
    privkey2reloaded = rsa.PrivateKey._load_pkcs1_der(priv_key_2_decoded)

    return privkey2reloaded


def load_public_key():
    drive = choose_drive()

    with open(drive + 'pub.pem') as f:
        pub_key_2 = f.read()

    pub_key_2_reloaded = rsa.PublicKey.load_pkcs1(pub_key_2.encode('utf8'))

    return pub_key_2_reloaded


def compute_hash(PIN):
    return rsa.compute_hash(PIN.encode('utf8'), 'SHA-256')



def cipher_w_aes(content, PIN):
    key = compute_hash(PIN)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    content = pad(content, 16)
    encrypted_content = cipher.encrypt(content)
    result = iv + encrypted_content
    return result


def decipher_w_aes(encrypted_content, PIN):
    key = compute_hash(PIN)
    iv = encrypted_content[:16]
    encrypted_content = encrypted_content[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_content = cipher.decrypt(encrypted_content)
    unpadded_content = unpad(decrypted_content, 16)
    return unpadded_content


def sign(hash, key):
    return rsa.sign_hash(hash, key, 'SHA-256')


def encrypt_with_rsa(content, key):
    signature = rsa.encrypt(content, key)

    with open('signature.sha256.rsa', 'wb') as f:
        f.write(signature)

    return signature


def decrypt_with_rsa(encrypted_content, key):
    with open(encrypted_content, 'rb') as f:
        fb = f.read()

    decrypted_content = rsa.decrypt(fb, key)
    return decrypted_content


def verify_signature(file, signature_file, public_key):
    with open(file, 'rb') as f:
        original = f.read()

    with open(signature_file, 'rb') as f:
        signature = f.read()

    try:
        rsa.verify(original, signature, public_key)
    except VerificationError:
        print("Podrobiono plik")
    else:
        print("Pliki się zgadzają")



def hash_file(file):
    with open(file, 'rb') as f:
        fb = f.read()

    _hash = rsa.compute_hash(fb, 'SHA-256')
    return _hash

print("Enter mode:\n" +
      "1. Generating & saving RSA keys\n" +
      "2. Loading & printing RSA keys\n" +
      "4. Signing & saving to a file\n" +
      "5. Veryfying signature\n"
      "6. Test general purpose encryption & decryption")

mode = input()

if mode == '1':
    gen_and_save_keys()

if mode == '2':
    loaded_pub_key = load_public_key()
    loaded_privkey = load_private_key()
    print(f"loaded pub key {loaded_pub_key}, loaded priv key {loaded_privkey}")

if mode == '4':
    loaded_priv_key = load_private_key()

    _hash = hash_file("requirements.txt")

    sign = sign(_hash, loaded_priv_key)

    with open('signature.sha256.rsa', 'wb') as f:
        f.write(sign)

if mode == '5':
    verify_signature("requirements.txt", "signature.sha256.rsa", load_public_key())

if mode == '6':
    gen_and_save_keys()

    file = "test.html"

    with open(file, 'rb') as f:
        fb = f.read()

    pub_key = load_public_key()

    encrypted_content = encrypt_with_rsa(fb, pub_key)

    with open(file + ".rsa", 'wb') as f:
        f.write(encrypted_content)

    with open(file + ".rsa", 'rb') as f:
        fb2 = f.read()

    priv_key = load_private_key()

    print(priv_key)

    decrypted_content = decrypt_with_rsa(fb2, priv_key)

    with open(file + "decrypted.html", 'wb') as f:
        f.write(decrypted_content)


def create_xml():
    import xml.etree.ElementTree as ET

    data = ET.Element('korzen')

    el1 = ET.SubElement(data, 'pierwszy')
    el2 = ET.SubElement(data, 'drugi')

    el3 = ET.SubElement(el1, 'trzeciWPierwszym')

    el1.text = 'tekst pierwszego'
    el2.text = 'tekst drugiego'
    el3.text = 'tekst trzeciego'

    el1.set('atrybut1', 'Wartosc')

    bxml = ET.tostring(data)

    with open("GFG.xml", "wb") as f:
        f.write(bxml)


