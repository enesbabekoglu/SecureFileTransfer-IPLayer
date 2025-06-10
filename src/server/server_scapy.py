from scapy.all import sniff, TCP, IP, Raw
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hashlib
from ..utils.config import AUTH_TOKEN

auth_token = AUTH_TOKEN

# === RSA Özel Anahtarı Yükle ===
def load_private_key():
    with open("server_private_key.pem", "rb") as key_file:
        return serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())

# === AES ile Şifre Çöz ===
def decrypt_file_with_aes(encrypted_data, aes_key, iv):
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_data) + decryptor.finalize()

# === SHA256 Hesapla ===
def calculate_sha256_from_bytes(data_bytes):
    sha256 = hashlib.sha256()
    sha256.update(data_bytes)
    return sha256.hexdigest().encode()

# === Gelen Paketi İşle ===
def packet_handler(packet):
    if packet.haslayer(Raw) and packet.haslayer(TCP):
        raw_data = packet[Raw].load
        try:
            token, encrypted_key, encrypted_data, received_hash = raw_data.split(b'||', 3)
        except ValueError:
            print("[!] Paket içeriği bölünemedi.")
            return

        if token != auth_token:
            print("[✘] Token doğrulama başarısız!")
            return

        print("[✔] Token doğrulandı.")

        try:
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

            decrypted_data = decrypt_file_with_aes(encrypted_data, aes_key, iv)
            calculated_hash = calculate_sha256_from_bytes(decrypted_data)

            if calculated_hash == received_hash:
                print("[✔] SHA256 doğrulaması başarılı.")
                with open("aliciya_ulaşan_dosya.txt", "wb") as f:
                    f.write(decrypted_data)
                print("[+] Dosya kaydedildi.")
            else:
                print("[✘] SHA256 doğrulaması başarısız!")
        except Exception as e:
            print(f"[!] Hata: {e}")

# === Scapy Sniff Başlat ===
print("[*] Scapy paketi bekleniyor (port 12345)...")
sniff(filter="tcp port 12345", prn=packet_handler, store=0)
