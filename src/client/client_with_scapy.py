from scapy.all import IP, TCP, Raw, send
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import hashlib

# Backend değişkenini bir kere tanımlayalım
backend = default_backend()

# === Ayarlar ===
file_to_send = "gonderilecek_dosya.txt"
server_ip = "127.0.0.1"
server_port = 12345
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
    with open("server_public_key.pem", "rb") as key_file:
        return serialization.load_pem_public_key(key_file.read(), backend=backend)

# === AES Key oluştur ve veriyi şifrele ===
def encrypt_file_with_aes(file_path, aes_key, iv):
    with open(file_path, "rb") as f:
        data = f.read()
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=backend)
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()
    return encrypted_data

# === Anahtar, IV ve veri hazırla ===
aes_key = os.urandom(32)
iv = os.urandom(16)
encrypted_data = encrypt_file_with_aes(file_to_send, aes_key, iv)

server_public_key = load_server_public_key()
encrypted_key = server_public_key.encrypt(
    aes_key + iv,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

file_hash = calculate_sha256(file_to_send)

# === Token + Encrypted Key + Encrypted Data + SHA256 Birlestir ===
final_data = auth_token + b'||' + encrypted_key + b'||' + encrypted_data + b'||' + file_hash

# === Scapy ile IP ve TCP başlığına gömerek gönder ===
packet = IP(dst=server_ip, ttl=44, flags="DF") / TCP(dport=server_port, sport=55555, flags="PA") / Raw(load=final_data)
send(packet)

print("[+] Scapy ile özel IP başlığı ve şifreli veri gönderildi.")
