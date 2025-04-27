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
git clone https://github.com/kullaniciadiniz/CryptoTransfer.git
cd CryptoTransfer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
