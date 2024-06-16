import rsa
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from ttp_helper import Helper # todo sprobowac zmienic na zwykly helper ale dodac glowne okno do tej apki wtedy
from globals import AES_BLOCK_SIZE
from globals import RSA_KEY_SIZE


class ttp():
    def __init__(self):
        self.helper = Helper()

    def cipher_w_aes(self, content, pin):
        key = self.helper.hash_pin(pin)
        iv = get_random_bytes(AES_BLOCK_SIZE)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        content = pad(content, AES_BLOCK_SIZE)
        encrypted_content = cipher.encrypt(content)
        result = iv + encrypted_content
        return result


    def generate_and_save_keys(self):
        location = self.helper.choose_directory("where to save keys")

        print("Gen and save keys location: ", location)

        (pub_key, priv_key) = rsa.newkeys(RSA_KEY_SIZE)

        with open(location + 'pub.pem', 'w') as f:
            f.write(pub_key.save_pkcs1().decode('utf8'))

        encrypted_key = self.cipher_w_aes(priv_key.save_pkcs1('DER'), self.helper.enter_pin())

        with open(location + 'priv.pem.aes', 'wb') as f:
            f.write(encrypted_key)


ttp().generate_and_save_keys()
