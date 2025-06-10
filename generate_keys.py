#!/usr/bin/env python3
"""
RSA anahtarları oluşturma betiği.
"""

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import os

# Keys dizinini oluştur
key_dir = "keys"
os.makedirs(key_dir, exist_ok=True)

# RSA key pair oluştur
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Private key'i PEM formatında kaydet
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

with open(os.path.join(key_dir, "server_private_key.pem"), "wb") as f:
    f.write(private_pem)

# Public key'i PEM formatında kaydet
public_key = private_key.public_key()
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

with open(os.path.join(key_dir, "server_public_key.pem"), "wb") as f:
    f.write(public_pem)

print("[+] RSA anahtarları başarıyla oluşturuldu:")
print(f"- Private key: keys/server_private_key.pem")
print(f"- Public key: keys/server_public_key.pem")
