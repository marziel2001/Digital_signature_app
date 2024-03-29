import hashlib
import sys

import rsa
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes
from hashlib import sha256



def gen_and_save_keys():
    print("please provide the drive letter")
    drive = input()

    (pub_key, priv_key) = rsa.newkeys(2048) # 4096 will be used to sign the hash
    #print(f"pub key {pub_key}, priv key {priv_key}")

    with open('pub.pem', 'w') as pubKeyFile:
        pubKeyFile.write(pub_key.save_pkcs1().decode('utf8'))

    encrypted_key = cipher_w_aes(priv_key.save_pkcs1('DER'), '1111')

    #todo in the end change path to drive/:priv.pem.aes
    with open(drive + 'priv.pem.aes', 'wb') as privKeyFile:
        privKeyFile.write(encrypted_key)


def load_keys():
    print("please provide the drive letter")
    drive = input()

    #todo in the end change path to drive/:priv.pem.aes
    with open(drive + 'priv.pem.aes', "rb") as privKeyFile:
        priv_key_2 = privKeyFile.read()

    with open('pub.pem') as pubKeyFile:
        pub_key_2 = pubKeyFile.read()

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


def encrypt_with_rsa(hash, key):
    signature = rsa.encrypt(hash, key)
    with open('signature.sha256.rsa', 'wb') as f:
        f.write(signature)


    print("len of signature: " + str(len(signature)))
    return signature


def verify_signature(file="./signature.sha256.rsa"):
    loaded_pub_key, loaded_privkey = load_keys()
    hash = hash_file()
    signature = encrypt_with_rsa(hash, loaded_pub_key)
    with open(file, "rb") as f:
        sig_to_check = f.read()

    if signature == sig_to_check:
        print("sygnatury się zgadzają!\n")


def hash_file(file="./requirements.txt"):
    BLOCK_SIZE = 65536

    hash = hashlib.sha256()
    with open(file, 'rb') as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            hash.update(fb)
            fb = f.read(BLOCK_SIZE)

    print("hash: " + hash.hexdigest())
    return hash.digest()

print("Enter mode:\n" +
      "1. Generating RSA keys\n" +
      "2. Loading keys\n" +
      "3. Encrypting a document\n")

mode = input()

if mode == '1':
    gen_and_save_keys()
if mode == '2':
    loaded_pub_key, loaded_privkey = load_keys()
    print(f"loaded pub key {loaded_pub_key}, loaded priv key {loaded_privkey}")
if mode == '3':
    hash_file()
if mode == '4':
    _, loaded_privkey = load_keys()
    hash = hash_file()
    encrypt_with_rsa(hash, loaded_privkey)
if mode == '5':
    verify_signature()




