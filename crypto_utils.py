from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

def generate_key(passphrase):
    if len(passphrase) < 4 or len(passphrase) > 10:
        raise ValueError("Password must be 4 to 10 characters long.")
    hashed = hashlib.sha256(passphrase.encode()).digest()
    return hashed[:16]

def encrypt_file(input_path, key, output_path):
    cipher = AES.new(key, AES.MODE_CBC)
    with open(input_path, "rb") as f:
        plaintext = f.read()
    padded = pad(plaintext, AES.block_size)
    ciphertext = cipher.iv + cipher.encrypt(padded)
    with open(output_path, "wb") as f:
        f.write(ciphertext)

def decrypt_file(input_path, key, output_path):
    with open(input_path, "rb") as f:
        ciphertext = f.read()
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext[AES.block_size:]), AES.block_size)
    with open(output_path, "wb") as f:
        f.write(plaintext)
