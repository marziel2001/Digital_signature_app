# Hash: SHA1
# Signature: RSA
# Signature private_key cipher: AES
import base64

import rsa
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes
from hashlib import sha256


def gen_and_save_keys():
    (pub_key, priv_key) = rsa.newkeys(256)  # 4096 will be used to sign the hash
    print(f'Public key: {pub_key}, \nPrivate key: {priv_key}')

    with open('pub.pem', 'w') as pubKeyFile:
        pubKeyFile.write(pub_key.save_pkcs1().decode('utf8'))

    encrypted_key = cipher_w_aes(priv_key.save_pkcs1('DER'), '1111')
    # print(f"encrypted key with aes:{encrypted_key}")

    with open('priv.pem.aes', 'wb') as privKeyFile:
        privKeyFile.write(encrypted_key)


def load_keys():
    with open('priv.pem.aes', "rb") as privKeyFile:
        priv_key_2 = privKeyFile.read()

    with open('pub.pem') as pubKeyFile:
        pub_key_2 = pubKeyFile.read()

    pub_key_2_reloaded = rsa.PublicKey.load_pkcs1(pub_key_2.encode('utf8'))

    #print(f"loaded priv key:{priv_key_2}")

    priv_key_2_decoded = decipher_w_aes(priv_key_2, '1111')

    #print(f"decrypted {priv_key_2_decoded}")
    privkey2reloaded = rsa.PrivateKey._load_pkcs1_der(priv_key_2_decoded)

    return pub_key_2_reloaded, privkey2reloaded

def compute_hash(PIN):
    return sha256(PIN.encode('utf8')).digest()


def cipher_w_aes(content, PIN):
    key = compute_hash(PIN)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    #print(f"cipher iv: {cipher.iv}")
    content = pad(content, 16)
    encrypted_content = cipher.encrypt(content)
    #print(f"iv: {iv} | cipher content{encrypted_content}")
    result = iv + encrypted_content
    #print(f"cipher result: {result}")
    return result


def decipher_w_aes(encrypted_content, PIN):
    key = compute_hash(PIN)
    iv = encrypted_content[:16]
    encrypted_content = encrypted_content[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    #print(f"iv2{cipher.iv}")
    decrypted_content = cipher.decrypt(encrypted_content)
    #print(f"after decrypting before unpad:{decrypted_content}")
    unpadded_content = unpad(decrypted_content, 16)
    return unpadded_content

gen_and_save_keys()
loaded_pub_key, loaded_privkey = load_keys()

print(f"loaded pub key {loaded_pub_key}, loaded priv key {loaded_privkey}")


