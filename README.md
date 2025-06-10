# SecureFileTransfer-IPLayer: Güvenli Ağ İletişim Aracı

Bu proje, istemci ve sunucu arasında güvenli dosya transferi sağlayan kapsamlı bir uygulamadır. Dosya içeriği AES ile şifrelenmekte, şifreli anahtar ise RSA algoritması kullanılarak güvenli şekilde aktarılmaktadır. Proje, TCP protokolü üzerinden düşük seviyeli, güvenli veri iletişimi sağlayarak, ağ üzerinden veri transferinde maksimum güvenlik sunmayı hedeflemektedir. Ayrıca, çeşitli ağ analizi araçları ve testleri ile ağ performansını izleme ve değerlendirme olanağı sunmaktadır.

## Özellikler

- **Güvenli Dosya Transferi**:
  - AES-CFB ile dosya içerik şifreleme
  - RSA-OAEP ile anahtar şifreleme
  - TCP protokolü üzerinden güvenli veri iletimi
  - Büyük dosyaların otomatik parçalanması ve bütünlük kontrolü
  - Şifrelenmiş veri transferi (plaintext koruması)

- **Ağ Analiz ve Test Araçları**:
  - IP başlık işleme ve analizi
  - Ping testleri ve RTT (Round Trip Time) ölçümleri
  - Bant genişliği ve performans testleri
  - Ağ koşulları simülasyonu ve karşılaştırması

- **Grafiksel Kullanıcı Arayüzü (GUI)**:
  - İstemci ve sunucu için sezgisel arayüzler
  - Ağ analiz aracı ile detaylı raporlama
  - MITM (Man-in-the-Middle) saldırı simülasyonu
  - Canlı performans grafikleri (Matplotlib ile)

## Kurulum

### Gereksinimleri Yükleme

```bash
git clone https://github.com/enesbabekoglu/SecureFileTransfer-IPLayer.git
cd SecureFileTransfer-IPLayer
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### RSA Anahtarlarını Oluşturma

Uygulama ilk kullanımda anahtarları otomatik oluşturacaktır, ancak manuel olarak da oluşturabilirsiniz:

```bash
python generate_keys.py
```

Veya OpenSSL ile manuel olarak:

```bash
mkdir -p keys
openssl genpkey -algorithm RSA -out keys/private_key.pem -pkeyopt rsa_keygen_bits:2048
openssl rsa -pubout -in keys/private_key.pem -out keys/public_key.pem
```

## Kullanım

### Ana Menü

Uygulamayı başlatmak için:

```bash
python -m src.gui.app
```

veya ana dizinde hazır betikleri kullanarak:

```bash
python run_client.py  # İstemci modunu başlatır
python run_server.py  # Sunucu modunu başlatır
```

Ana menüde dört farklı mod seçeneği bulunmaktadır:

1. **Sunucu Modu**: Dosya alımı için sunucu başlatır
2. **İstemci Modu**: Dosya göndermek için istemci başlatır
3. **Ağ Analizi**: Ağ performansını test etme araçları sunar
4. **MITM Saldırısı**: Man-in-the-Middle saldırı simülasyonu yapar

## Gereksinimler

- Python 3.8+
- Temel kütüphaneler:
  - cryptography (>=41.0.0)
  - scapy (>=2.5.0)
  - pytest (>=7.0.0)
  - matplotlib (>=3.7.0) - Grafikler için 
  - pymongo (>=4.3.0) - Veri depolama için
  - pycryptodome (>=3.17.0) - Ek kriptografi fonksiyonları için
  - python-dotenv (>=1.0.0)
  - requests (>=2.28.0)
  - PyQt5 (>=5.15.0) - Opsiyonel, gelişmiş UI için
  - numpy (>=1.24.0) - Veri analizi için

## Modüller ve Detaylı Kullanım

### 1. İstemci Modu (Client Mode)

İstemci modu, dosya gönderimi için kullanılan arayüzdür.

```bash
python run_client.py
```

**Kullanım Adımları:**

1. **Sunucu Bağlantı Ayarları:**
   - Sunucu IP: Bağlanılacak sunucunun IP adresi (varsayılan: 127.0.0.1)
   - Port: Sunucunun dinlediği port (varsayılan: 10000)
   - Token: Kimlik doğrulama için kullanılan şifre

2. **Sunucuya Bağlan** butonuna tıklayarak bağlantı test edilir. Başarılı bağlantı durumunda yeşil onay işareti görünür.

3. **Dosya Seç** butonu ile göndermek istediğiniz dosyayı seçin.

4. **Dosyayı Gönder** butonu ile seçilen dosya şifrelenerek sunucuya gönderilir.

5. Transfer sırasında transfer durumu ekranda görüntülenir.

### 2. Sunucu Modu (Server Mode)

Sunucu modu, dosya alımı için kullanılır.

```bash
python run_server.py
```

**Kullanım Adımları:**

1. **Sunucuyu Başlat** butonuna tıklayarak sunucuyu dinleme moduna alın. Port 10000 üzerinden bağlantıları dinler.

2. Log ekranında bağlantı ve dosya alım durumları görüntülenir.

3. Alınan dosyalar, projenin kök dizininde oluşturulan "received_files" klasörüne kaydedilir.

### 3. Ağ Analizi (Network Analysis)

Ağ analiz aracı, ağ performansını ve durumunu analiz etmek için kullanılır.

**Sekme 1: IP Başlık İşleme**
- IP başlıklarını oluşturma, inceleme ve test etme
- Paket fragmentasyonu ve checksum hesaplamaları yapma

**Sekme 2: Ping Testi**
- Belirtilen IP adresine ping atarak RTT ölçümü
- Sonuçları grafik olarak görselleştirme
- Paket kaybı ve gecikme istatistikleri görüntüleme

**Sekme 3: Bant Genişliği Testi**
- Upload/Download hızı ölçümü
- TCP/UDP protokollerini kullanarak bant genişliği testi
- Test sonuçlarını detaylı raporlama

**Sekme 4: Ağ Koşulları Simülasyonu**
- Farklı ağ koşullarını simüle etme (paket kaybı, gecikme)
- Ağ performansını karşılaştırma
- Optimizasyon önerileri sunma

### 4. MITM Saldırı Simülasyonu

MITM (Man-in-the-Middle) saldırısını simüle ederek, güvenlik açıklarını tespit etmeye yardımcı olur.

**Özellikler:**
- ARP zehirleme simülasyonu
- Şifrelenmemiş trafiği izleme
- Şifreli trafiğin analizi
- Güvenlik önlemleri test etme

## Proje Yapısı

```
Secure/
├── keys/                 # RSA anahtar dosyaları
│   ├── private_key.pem   # Özel anahtar
│   └── public_key.pem    # Genel anahtar
├── src/                  # Kaynak kodlar
│   ├── client/           # İstemci modülleri
│   ├── gui/              # Grafik arayüz dosyaları
│   ├── proxy/            # MITM ve proxy modülleri
│   ├── server/           # Sunucu modülleri
│   └── utils/            # Yardımcı fonksiyonlar
├── README.md             # Bu dosya
├── generate_keys.py      # Anahtar üretim betiği
├── requirements.txt      # Bağımlılıklar
├── run_client.py         # İstemci başlatma betiği
└── run_server.py         # Sunucu başlatma betiği
```

## Güvenlik Özellikleri

- **End-to-End Şifreleme**: Dosyalar AES-CFB (256 bit) ile şifrelenir, şifreleme anahtarı RSA-OAEP (2048 bit) ile korunur.

- **Bütünlük Kontrolü**: Her dosya parçası için SHA-256 hash değeri hesaplanır ve alıcı tarafında doğrulanır.

- **Parçalı Transfer**: Büyük dosyalar otomatik olarak parçalanır ve her parça ayrı şifrelenir, bu sayede bellek verimliliği sağlanır.

- **Token Doğrulama**: İstemci ve sunucu arasındaki iletişim, önceden belirlenmiş tokenlar ile güvence altına alınır.

## Sorun Giderme

### Bağlantı Sorunları

- Port kullanımda hatası alırsanız, farklı bir port kullanmayı deneyin.
- Bağlantı zaman aşımı sorunu yaşıyorsanız, güvenlik duvarı ayarlarınızı kontrol edin.

### Şifreleme Hataları

- "Key file not found" hatası alırsanız, `generate_keys.py` betiğini çalıştırın.
- Şifre çözme hatası olursa, şifreleme anahtarlarının doğru olduğundan emin olun.

## Test Senaryoları

Aşağıdaki test senaryolarını kullanarak sistemin çeşitli özelliklerini test edebilirsiniz.

### Temel Dosya Transferi Testi

1. Sunucu modunu başlatın: `python run_server.py`
2. Farklı bir terminalde istemci modunu başlatın: `python run_client.py`
3. Küçük bir metin dosyası oluşturun ve gönderin. Örnek:

```bash
echo "Bu bir test dosyasıdır" > test_dosya.txt
```

4. Sunucu loglarında dosyanın alındığını kontrol edin
5. `received_files` klasöründe dosyanın var olduğundan emin olun

### Büyük Dosya Transferi Testi

Büyük dosya parçalanmasını test etmek için:

```bash
# 50MB test dosyası oluştur (Linux/Mac):
head -c 50M < /dev/urandom > buyuk_dosya.test

# Windows için PowerShell komutu:
# fsutil file createnew buyuk_dosya.test 52428800
```

Dosyayı istemci ile gönderip, sunucuda doğru şekilde alınıp alınmadığını kontrol edin.

### Ağ Performans Testi

Bant genişliği ve gecikme testleri yapmak için:

1. Ana menüden "Ağ Analizi" modülünü seçin
2. "Bant Genişliği Testi" sekmesinden test parametrelerini ayarlayın
3. Yerel ağ veya internet bağlantısını test edin

### Güvenlik Testi

MITM saldırısını simüle etmek için:

1. Ana menüden "MITM Saldırısı" modülünü seçin
2. Hedef IP adreslerini belirleyin
3. Paket yakalama fonksiyonunu başlatın
4. Ayrı bir istemci ve sunucu ile dosya transferi yapın
5. Şifreli veri paketlerinin güvenli bir şekilde transfer edilip edilmediğini kontrol edin

## Gelişmiş Özellikler ve İpuçları

### Özelleştirilmiş Şifreleme Parametreleri

`src/utils/cryptography_utils.py` dosyasında şifreleme parametrelerini düzenleyebilirsiniz. Örneğin, AES anahtar boyutunu veya şifreleme modunu değiştirmek için:

```python
KEY_SIZE = 32  # 256 bit (varsayılan)
IV_SIZE = 16   # 128 bit
```

### Otomatik Test Koşturma

Pytest ile tüm testleri çalıştırmak için:

```bash
python -m pytest
```

Belirli bir testi çalıştırmak için:

```bash
python -m pytest test_chunked_transfer.py
```

### Performans İzleme

Ağ analizi sırasında performans ve kaynak kullanımını izleyebilirsiniz. Bunun için ağ analiz modülündeki "Bant Genişliği Testi" sekmesini kullanabilirsiniz. 

Teşekkederim.

## İletişim ve Katkıda Bulunma

Projeye katkıda bulunmak veya sorularınız için GitHub üzerinden iletişime geçebilirsiniz. Ana projeye erişmek için:

```bash
git clone https://github.com/enesbabekoglu/SecureFileTransfer-IPLayer.git
```
