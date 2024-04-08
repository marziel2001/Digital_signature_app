import hashlib
import rsa
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes
from hashlib import sha256

SHA_BLOCK_SIZE = 65536


def choose_drive():
    print("please provide the drive letter")
    drive = input()

    if drive is not "":
        drive += "/"

    return drive


def gen_and_save_keys():
    drive = choose_drive()

    (pub_key, priv_key) = rsa.newkeys(2048) # 4096 will be used to sign the hash
    #print(f"pub key {pub_key}, priv key {priv_key}")

    with open(drive + 'pub.pem', 'w') as pubKeyFile:
        pubKeyFile.write(pub_key.save_pkcs1().decode('utf8'))

    encrypted_key = cipher_w_aes(priv_key.save_pkcs1('DER'), '1111')

    with open(drive + 'priv.pem.aes', 'wb') as privKeyFile:
        privKeyFile.write(encrypted_key)

    with open(drive + 'priv.pem', 'w') as f:
        f.write(priv_key.save_pkcs1().decode('utf8'))


def load_keys():
    drive = choose_drive()

    with open(drive + 'priv.pem.aes', "rb") as f:
        priv_key_2 = f.read()

    with open('pub.pem') as f:
        pub_key_2 = f.read()

    pub_key_2_reloaded = rsa.PublicKey.load_pkcs1(pub_key_2.encode('utf8'))

    priv_key_2_decoded = decipher_w_aes(priv_key_2, '1111')
    privkey2reloaded = rsa.PrivateKey._load_pkcs1_der(priv_key_2_decoded)

    return pub_key_2_reloaded, privkey2reloaded


def compute_hash(PIN):
    return sha256(PIN.encode('utf8')).digest()


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


def encrypt_with_rsa(content, key):
    signature = rsa.encrypt(content, key)
    return signature


def decrypt_with_rsa(encrypted_content, key):
    decrypted_content = rsa.decrypt(encrypted_content, key)
    return decrypted_content


def verify_signature(signature_file, public_key):
    # computing hash of received file
    our_hash = hash_file()

    # decrypting received hash
    their_hash = decrypt_with_rsa(signature_file, public_key)

    if our_hash == their_hash:
        print("hashes match!")
    else:
        print("somebody tried to trick us!")


def hash_file(file):
    _hash = hashlib.sha256()
    with open(file, 'rb') as f:
        fb = f.read(SHA_BLOCK_SIZE)
        while len(fb) > 0:
            _hash.update(fb)
            fb = f.read(SHA_BLOCK_SIZE)

    print("hash: " + _hash.hexdigest())
    return _hash.digest()

print("Enter mode:\n" +
      "1. Generating & saving RSA keys\n" +
      "2. Loading & printing RSA keys\n" +
      "3. Hashing\n" +
      "4. Signing & saving to a file\n" +
      "5. Veryfying signature\n")

mode = input()

if mode == '1':
    gen_and_save_keys()

if mode == '2':
    loaded_pub_key, loaded_privkey = load_keys()
    print(f"loaded pub key {loaded_pub_key}, loaded priv key {loaded_privkey}")

if mode == '3':
    hash_file()

if mode == '4':
    _, loaded_priv_key = load_keys()
    _hash = hash_file()
    sign = encrypt_with_rsa(_hash, loaded_priv_key)

    with open('signature.sha256.rsa', 'wb') as f:
        f.write(sign)

if mode == '5':
    verify_signature()
