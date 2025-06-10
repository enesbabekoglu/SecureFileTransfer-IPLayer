# 🔐 Güvenli Dosya Transfer Sistemi (SecureFileTransfer-IPLayer)

## 📋 Proje Hakkında

Bu proje, düşük seviyeli IP katmanı manipülasyonu ile güvenli dosya transferi gerçekleştiren bir sistemdir. Geleneksel dosya transferlerinden farklı olarak, ağ paketlerini doğrudan işleyerek güvenlik, performans analizi ve çeşitli ağ koşullarında dosya aktarımı testleri yapabilmenizi sağlar.

## ✨ Temel Özellikler

### 🗂️ Dosya Transfer Sistemi
- 📤 Ağ üzerinden dosya gönderme ve alma desteği
- 📦 Büyük dosya transferleri için manuel paket parçalama ve birleştirme
- 🛠️ Hasarlı veya kayıp paketler için hata tespit ve düzeltme mekanizmaları

### 🔒 Güvenlik Mekanizmaları
- 🔐 İletim sırasında dosyaları korumak için AES/RSA şifreleme
- 🛂 Transferden önce istemci kimlik doğrulaması
- ✅ SHA-256 ile bütünlük doğrulaması

### 📡 Düşük Seviyeli IP Başlık İşleme
- 📝 IP başlıklarını (bayraklar, TTL, sağlama toplamı, parçalama) manuel olarak düzenleme
- 🧮 İletim öncesi IP sağlama toplamını hesaplama ve doğrulama
- 🧩 Alıcı tarafında paket birleştirme analizi

### 📊 Ağ Performans Ölçümü
- ⏱️ Gecikme ölçümü (ping, RTT hesaplamaları)
- 📈 iPerf ve paket analizi ile bant genişliği ölçümü
- 🚦 tc kullanarak paket kaybı ve ağ tıkanıklığı simülasyonu
- 📡 Farklı ağ koşullarının karşılaştırılması (Wi-Fi vs kablolu, yerel vs uzak)

### 🛡️ Güvenlik Analizi ve Saldırı Simülasyonu
- 🕵️ Wireshark ile paketleri yakalama ve analiz etme
- 🥷 Araya girme (MITM) ve paket enjeksiyonu saldırıları simülasyonu
- 🔐 Şifreleme ile paket yakalamalarda verilerin okunamaz olması sağlama

### 🖥️ Kullanıcı Arayüzü
- 📱 Grafiksel arayüz (GUI) ile kolay kullanım
- 📊 Transfer durumu ve detaylı istatistikler görselleştirme
- 📝 Ağ analizleri için görsel raporlama

## 🔧 Teknoloji Yığını

- **Programlama Dili**: Python
- **Ağ Paket İşleme**: Scapy
- **Şifreleme Kütüphaneleri**: cryptography, hashlib
- **Grafiksel Arayüz**: PyQt5
- **Veri Görselleştirme**: matplotlib
- **Ağ Analiz Araçları**: Wireshark, tc

## 🚀 Kurulum

### 📋 Gereksinimler

- Python 3.7+
- pip paket yöneticisi
- Gerekli kütüphaneler için `requirements.txt` dosyası

### ⚙️ Kurulum Adımları

1. **Projeyi İndirin**:
   ```bash
   git clone https://github.com/enesbabekoglu/SecureFileTransfer-IPLayer.git
   cd SecureFileTransfer-IPLayer
   ```

2. **Sanal Ortam Oluşturun** (Opsiyonel ama önerilen):
   ```bash
   python -m venv venv
   
   # Windows için:
   venv\Scripts\activate
   
   # Linux/Mac için:
   source venv/bin/activate
   ```

3. **Gerekli Kütüphaneleri Yükleyin**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Anahtar Çiftlerini Oluşturun**:
   ```bash
   python generate_keys.py
   ```
   Bu komut `keys` dizininde RSA anahtar çiftleri oluşturacak.

## 🎮 Kullanım

### 🚀 Başlatma

Projeyi başlatmak için sağlanan script dosyalarından birini çalıştırabilirsiniz:

**Linux/Mac için**:
```bash
./baslat.sh
```

**Windows için**:
```bash
baslat.bat
```

### 💻 Kullanım Senaryoları

#### 1️⃣ Dosya Transferi

1. Ana menüden "Sunucu Modu"nu başlatın
2. Başka bir bilgisayardan "İstemci Modu"nu başlatın
3. İstemci modunda:
   - Sunucu IP adresini girin
   - Göndermek istediğiniz dosyayı seçin
   - İsteğe bağlı güvenlik ayarlarını yapın
   - "Gönder" butonuna tıklayın
4. Transfer durumunu arayüzden takip edin

#### 2️⃣ Ağ Performans Analizi

1. Ana menüden "Ağ Analizi" seçeneğini seçin
2. İlgilendiğiniz hedef IP adresini girin
3. Aşağıdaki testlerden birini uygulayın:
   - RTT ölçümü
   - Bant genişliği testi
   - Paket kaybı simülasyonu
4. Sonuçları grafiksel olarak görüntüleyin

#### 3️⃣ MITM Saldırısı Simülasyonu

1. Ana menüden "MITM Saldırısı" seçeneğini seçin
2. Hedef IP adresini ve saldırı tipini seçin
3. Saldırıyı başlatın ve yakalanan paketleri analiz edin
4. Şifrelemenin etkisini gözlemleyin

## 🔍 Özellikler Detayı

### 🧩 Hibrit TCP/UDP Geçişi
Sistem, ağ koşullarına göre TCP veya UDP protokollerini dinamik olarak seçebilir, böylece ağ performansını optimize edebilir.

### 🚦 Dinamik Tıkanıklık Kontrolü
Transfer hızı, mevcut ağ koşullarına göre otomatik olarak ayarlanarak verimli bant genişliği kullanımı sağlar.

### 🔍 Gerçek Zamanlı Paket Analizi
Transfer sırasında paketlerin durumu, gecikmeleri ve bütünlüğü gerçek zamanlı olarak izlenebilir.

## 🤝 Katkı

Bu projeye katkıda bulunmak isterseniz:

1. Projeyi fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik: xyz'`)
4. Branch'inizi push edin (`git push origin feature/yeni-ozellik`)
5. Pull Request açın

## 📜 Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.

---

📧 İletişim: enes@example.com
🌐 GitHub: [github.com/enesbabekoglu](https://github.com/enesbabekoglu)
