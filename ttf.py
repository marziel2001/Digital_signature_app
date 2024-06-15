import rsa
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from helper import choose_directory
from helper import hash_pin
from helper import enter_pin
from globals import AES_BLOCK_SIZE
from globals import RSA_KEY_SIZE


def cipher_w_aes(content, pin):
    key = hash_pin(pin)
    iv = get_random_bytes(AES_BLOCK_SIZE)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    content = pad(content, AES_BLOCK_SIZE)
    encrypted_content = cipher.encrypt(content)
    result = iv + encrypted_content
    return result


def generate_and_save_keys():
    location = choose_directory()

    print(location)

    (pub_key, priv_key) = rsa.newkeys(RSA_KEY_SIZE)

    with open(location + 'pub.pem', 'w') as f:
        f.write(pub_key.save_pkcs1().decode('utf8'))

    encrypted_key = cipher_w_aes(priv_key.save_pkcs1('DER'), enter_pin())

    with open(location + 'priv.pem.aes', 'wb') as f:
        f.write(encrypted_key)


generate_and_save_keys()
