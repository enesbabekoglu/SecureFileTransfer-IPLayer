import socket
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import hashlib

# Global olarak backend'i bir kez tanımlayalım
backend = default_backend()

# === Ayarlar ===
file_to_send = "gonderilecek_dosya.txt"
server_ip = "127.0.0.1"
server_port = 10000  # proxy portu (normalde 12345'ti)
auth_token = b"gizli_token_123"

# === SHA-256 Hesapla ===
def calculate_sha256(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest().encode()

# === RSA Anahtarını Yükle ===
def load_server_public_key():
    with open("keys/server_public_key.pem", "rb") as key_file:
        return serialization.load_pem_public_key(key_file.read(), backend=backend)

# === AES Key oluştur ve veriyi şifrele ===
def encrypt_file_with_aes(file_path, aes_key, iv):
    with open(file_path, "rb") as f:
        data = f.read()
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=backend)
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()
    return encrypted_data

# === Bağlantı Kur ===
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# === Token Gönder ===
client_socket.sendall(auth_token + b"\n")

# === AES Key ve IV oluştur ===
aes_key = os.urandom(32)
iv = os.urandom(16)

# === Dosyayı AES ile şifrele ===
encrypted_data = encrypt_file_with_aes(file_to_send, aes_key, iv)

# === AES Key'i RSA ile şifrele ===
server_public_key = load_server_public_key()
encrypted_key = server_public_key.encrypt(
    aes_key + iv,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# === Dosya hash’ini hesapla ===
file_hash = calculate_sha256(file_to_send)

# === Final veri formatı: EncryptedKey || EncryptedData || FileHash ===
final_data = encrypted_key + b'||' + encrypted_data + b'||' + file_hash

# === Gönder ===
client_socket.sendall(final_data)
print("[+] Token, dosya ve SHA-256 hash gönderildi.")

client_socket.close()
