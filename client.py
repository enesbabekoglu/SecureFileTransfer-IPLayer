import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import os

SERVER_IP = '127.0.0.1'
SERVER_PORT = 9000

# AES Anahtarı oluştur
aes_key = os.urandom(32)  # 256-bit AES anahtarı

# Dosya oku ve AES ile şifrele
def encrypt_file(filename, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    with open(filename, 'rb') as f:
        data = f.read()
    return iv + encryptor.update(data) + encryptor.finalize()

# AES anahtarını RSA ile şifrele
def encrypt_aes_key(public_key_path, key):
    with open(public_key_path, 'rb') as f:
        public_key = serialization.load_pem_public_key(f.read())
    encrypted_key = public_key.encrypt(
        key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    return encrypted_key

# Şifrele
encrypted_file = encrypt_file('gonderilecek_dosya.txt', aes_key)
encrypted_aes_key = encrypt_aes_key('keys/public_key.pem', aes_key)

# Socket ile gönder
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((SERVER_IP, SERVER_PORT))
    s.sendall(encrypted_aes_key)
    s.sendall(encrypted_file)
