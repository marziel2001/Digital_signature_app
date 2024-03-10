# Hash: SHA1
# Signature: RSA
# Signature private_key cipher: AES
import rsa


def gen_and_save_keys():
    (pub_key, priv_key) = rsa.newkeys(256)  # 4096 will be used to sign the hash

    with open('priv.pem', 'w') as privKeyFile:
        privKeyFile.write(priv_key.save_pkcs1().decode('utf8'))

    with open('pub.pem', 'w') as pubKeyFile:
        pubKeyFile.write(pub_key.save_pkcs1().decode('utf8'))


def load_keys():
    with open('priv.pem') as privKeyFile:
        privkey2 = privKeyFile.read()

    with open('pub.pem') as pubKeyFile:
        pubkey2 = pubKeyFile.read()

    pubkey2reloaded = rsa.PublicKey.load_pkcs1(pubkey2.encode('utf8'))
    privkey2reloaded = rsa.PrivateKey.load_pkcs1(privkey2.encode('utf8'))

    return pubkey2reloaded, privkey2reloaded


gen_and_save_keys()
pubk, privk = load_keys()

print(pubk)
print(privk)