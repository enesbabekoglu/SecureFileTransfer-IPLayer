# SecureFileTransfer-IPLayer
Bu proje istemci ve sunucu arasında güvenli dosya transferi sağlayan bir uygulamadır. Dosya içeriği AES ile şifrelenmekte, şifreli anahtar ise RSA algoritması kullanılarak güvenli şekilde aktarılmaktadır. Proje, TCP protokolü üzerinden düşük seviyeli, güvenli veri iletişimi sağlamayı hedeflemektedir.

## Özellikler

- AES-CFB ile dosya şifreleme
- RSA-OAEP ile anahtar şifreleme
- TCP protokolü üzerinden veri iletimi
- Wireshark ile ağ trafiği analizi
- Şifrelenmiş veri transferi (plaintext koruması)

## Kurulum

```bash
git clone https://github.com/enesbabekoglu/SecureFileTransfer-IPLayer.git
cd SecureFileTransfer-IPLayer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Kullanım

Öncelikle RSA anahtarlarını oluşturun:

```bash
mkdir keys
openssl genpkey -algorithm RSA -out keys/private_key.pem -pkeyopt rsa_keygen_bits:2048
openssl rsa -pubout -in keys/private_key.pem -out keys/public_key.pem
```

Sunucuyu başlatın:

```bash
python3 server.py
```

Başka bir terminalde istemciyi başlatın:

```bash
python3 client.py
```

## Gereksinimler

- Python 3.8+
- cryptography
- scapy
- pytest
