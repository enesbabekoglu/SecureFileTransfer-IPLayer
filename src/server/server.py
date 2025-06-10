import socket
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hashlib
from ..utils.config import AUTH_TOKEN

# Backend değişkenini bir kez tanımlayalım
backend = default_backend()

# === Token Doğrulama ===
auth_token = AUTH_TOKEN

# === SHA-256 Hesaplama Fonksiyonu ===
def calculate_sha256_from_bytes(data_bytes):
    sha256 = hashlib.sha256()
    sha256.update(data_bytes)
    return sha256.hexdigest().encode()

# === RSA Özel Anahtarı Yükle ===
def load_private_key():
    with open("keys/server_private_key.pem", "rb") as key_file:
        return serialization.load_pem_private_key(key_file.read(), password=None, backend=backend)

# === AES ile Şifre Çöz ===
def decrypt_file_with_aes(encrypted_data, aes_key, iv):
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=backend)
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_data) + decryptor.finalize()

# === Bağlantıyı Dinle ===
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 12345))
server_socket.listen(1)
print("[*] Sunucu dinleniyor...")

conn, addr = server_socket.accept()
print(f"[+] Bağlantı alındı: {addr}")

# === Token Doğrulama ===
token = conn.recv(1024).strip()
if token != auth_token:
    print("[✘] Geçersiz token! Bağlantı reddedildi.")
    conn.close()
    exit()
else:
    print("[✔] Token doğrulandı.")

# === Veriyi Al ===
data = b""
while True:
    chunk = conn.recv(4096)
    if not chunk:
        break
    data += chunk

conn.close()

# === Veriyi Ayır ===
try:
    encrypted_key, encrypted_data, received_hash = data.split(b'||')
except ValueError:
    print("[!] Hatalı veri formatı. Ayırma işlemi başarısız.")
    exit()

# === RSA ile AES Anahtarını ve IV'yi çöz ===
private_key = load_private_key()
decrypted_key_iv = private_key.decrypt(
    encrypted_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
aes_key = decrypted_key_iv[:32]
iv = decrypted_key_iv[32:]

# === AES ile Dosya Verisini Çöz ===
decrypted_data = decrypt_file_with_aes(encrypted_data, aes_key, iv)

# === SHA-256 Kontrolü ===
calculated_hash = calculate_sha256_from_bytes(decrypted_data)

if calculated_hash == received_hash:
    print("[✔] SHA-256 doğrulaması başarılı. Dosya bozulmamış.")
    with open("aliciya_ulaşan_dosya.txt", "wb") as f:
        f.write(decrypted_data)
    print("[+] Dosya başarıyla kaydedildi.")
else:
    print("[✘] SHA-256 doğrulaması başarısız! Dosya bozulmuş olabilir.")
