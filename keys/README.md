# Güvenlik Anahtarları Klasörü

Bu klasör, güvenli dosya transferi için gerekli RSA anahtarlarını içerir.

## Anahtar Oluşturma

Anahtarları oluşturmak için, projenin kök dizinindeki `generate_keys.py` scriptini çalıştırın:

```bash
python generate_keys.py
```

Bu işlem aşağıdaki dosyaları oluşturacaktır:
- `server_public_key.pem` - Sunucu için genel anahtar 
- `server_private_key.pem` - Sunucu için özel anahtar

## Güvenlik Notları

- Özel anahtarları (.pem dosyalarını) asla GitHub'a yüklemeyin
- Dosya transferi için yeni anahtarlar oluşturun
- Bu anahtarlar sadece test ve eğitim amaçlıdır
