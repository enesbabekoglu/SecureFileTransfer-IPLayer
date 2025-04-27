import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import os

SERVER_IP = '0.0.0.0'
SERVER_PORT = 9000

# RSA ile AES anahtarını çöz
def decrypt_aes_key(private_key_path, encrypted_key):
    with open(private_key_path, 'rb') as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)
    aes_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    return aes_key

# Dosyayı AES ile çöz
def decrypt_file(encrypted_data, key):
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()

# Bağlantı başlat
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((SERVER_IP, SERVER_PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        encrypted_key = conn.recv(256)   # RSA şifreli AES anahtarı
        encrypted_data = b''
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            encrypted_data += chunk

        aes_key = decrypt_aes_key('keys/private_key.pem', encrypted_key)
        original_data = decrypt_file(encrypted_data, aes_key)

        with open('alınan_dosya.txt', 'wb') as f:
            f.write(original_data)
