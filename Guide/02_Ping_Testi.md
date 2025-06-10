# Ping Testi Kılavuzu

Bu kılavuz, SecureFileTransfer-IPLayer projesindeki Ping Testi özelliklerini ayrıntılı şekilde açıklamaktadır. Bu modül, ağ bağlantısının durumunu, gecikmesini ve kararlılığını değerlendirmenize olanak tanır.

## İçerik

1. [Genel Bakış](#genel-bakış)
2. [Arayüz Tanıtımı](#arayüz-tanıtımı)
3. [Ping Testi Parametreleri](#ping-testi-parametreleri)
4. [Test Sonuçlarını Yorumlama](#test-sonuçlarını-yorumlama)
5. [Grafik Görselleştirme](#grafik-görselleştirme)
6. [İstatistiksel Analiz](#istatistiksel-analiz)
7. [Örnek Kullanım Senaryoları](#örnek-kullanım-senaryoları)
8. [Sorun Giderme](#sorun-giderme)

## Genel Bakış

Ping Testi, ICMP Echo Request ve Echo Reply paketleri kullanarak hedef bir bilgisayara olan bağlantının durumunu ve performansını ölçen bir araçtır. Bu test sayesinde:

- İki nokta arasındaki gidiş-dönüş süresini (RTT - Round Trip Time) ölçebilirsiniz
- Paket kaybı oranını tespit edebilirsiniz
- Ağ bağlantısının kararlılığını değerlendirebilirsiniz
- Bağlantı kalitesini zaman içinde izleyebilirsiniz

## Arayüz Tanıtımı

Ağ Analiz aracının "Ping Testi" sekmesi aşağıdaki bölümlerden oluşur:

- **Hedef IP/Hostname**: Ping atılacak hedef sunucunun IP adresi veya alan adı
- **Ping Sayısı**: Gönderilecek ping paketi sayısı
- **Zaman Aşımı (ms)**: Her ping için beklenecek maksimum yanıt süresi
- **Paket Boyutu (bytes)**: Ping paketlerinin içerebileceği veri miktarı
- **Bekleme Süresi (ms)**: Ping paketleri arasındaki bekleme süresi
- **Testi Başlat**: Ping testini başlatma butonu
- **Sonuç Alanı**: Test sonuçlarının gösterildiği metin alanı
- **Grafik Alanı**: RTT değerlerinin zaman içindeki değişiminin grafik gösterimi

## Ping Testi Parametreleri

### Hedef IP/Hostname

- **Format**: IPv4 adresi (örn. "8.8.8.8") veya alan adı (örn. "google.com")
- **Önerilen Değerler**: 
  - Yerel ağ testleri için gateway IP'si (örn. "192.168.1.1")
  - İnternet testi için güvenilir sunucular (örn. "8.8.8.8" veya "1.1.1.1")

### Ping Sayısı

- **Aralık**: 1-10000
- **Varsayılan**: 10
- **Öneriler**:
  - Hızlı test için: 5-10 ping
  - Standart test için: 20-50 ping
  - Uzun süreli stabilite testi için: 100+ ping

### Zaman Aşımı (ms)

- **Aralık**: 100-10000 ms
- **Varsayılan**: 1000 ms (1 saniye)
- **Öneriler**:
  - Yerel ağ için: 500 ms
  - Geniş alan ağı için: 1000-2000 ms
  - Uluslararası bağlantılar için: 3000+ ms

### Paket Boyutu (bytes)

- **Aralık**: 32-65500 bytes
- **Varsayılan**: 56 bytes (ICMP başlık boyutu hariç)
- **Öneriler**:
  - Standart test için: 56 bytes
  - MTU sorunlarını tespit için: 1472 bytes
  - Bant genişliği etkisini test için: 8192+ bytes

### Bekleme Süresi (ms)

- **Aralık**: 0-5000 ms
- **Varsayılan**: 1000 ms (1 saniye)
- **Öneriler**:
  - Hızlı test için: 200-500 ms
  - Standart test için: 1000 ms
  - Düşük bant genişliğini simüle için: 2000+ ms

## Test Sonuçlarını Yorumlama

Ping testi sonuçları aşağıdaki metrikleri içerir:

### RTT (Round Trip Time)

- **Minimum RTT**: En hızlı yanıt süresi
- **Maksimum RTT**: En yavaş yanıt süresi
- **Ortalama RTT**: Tüm yanıtların ortalama süresi
- **Standart Sapma**: RTT değerlerinin kararlılığının bir göstergesi

#### İyi RTT Değerleri:
- **Yerel Ağ**: < 1 ms
- **Aynı Şehir**: 5-30 ms
- **Aynı Ülke**: 10-60 ms
- **Kıtalararası**: 100-300 ms

### Paket Kaybı

- **Hesaplama**: (Gönderilen paket sayısı - Alınan yanıt sayısı) / Gönderilen paket sayısı * 100
- **İyi Değerler**: %0-1 arası
- **Kabul Edilebilir**: %1-5 arası
- **Sorunlu**: %5+ üzeri

### Jitter (Gecikme Değişimi)

- **Hesaplama**: RTT değerlerinin standart sapması
- **İyi Değerler**: < 5 ms
- **Kabul Edilebilir**: 5-30 ms
- **Sorunlu**: > 30 ms

## Grafik Görselleştirme

Ping sonuçları, zaman serisi grafiği olarak görselleştirilir:

- **X Ekseni**: Ping sırası (1'den başlayarak)
- **Y Ekseni**: RTT değeri (milisaniye)
- **Mavi Çizgi**: Her ping için ölçülen RTT değeri
- **Kırmızı Çizgi** (opsiyonel): Ortalama RTT değeri
- **Kırmızı Noktalar**: Paket kaybı veya zaman aşımı

### Grafik İşlevleri

- **Yakınlaştırma/Uzaklaştırma**: Fare tekerleği ile grafik üzerinde yakınlaştırma yapabilirsiniz
- **Kaydırma**: Grafik üzerinde sol tıklayarak sürükleme yapabilirsiniz
- **Veri Noktası İnceleme**: Grafik üzerindeki noktalara fare ile geldiğinizde tam değeri görebilirsiniz

## İstatistiksel Analiz

Test tamamlandıktan sonra aşağıdaki istatistikler otomatik olarak hesaplanır:

- **Gönderilen ping sayısı**: Toplam gönderilen ICMP Echo Request paketi sayısı
- **Alınan yanıt sayısı**: Toplam alınan ICMP Echo Reply paketi sayısı
- **Paket kaybı (%)**: Kayıp paket yüzdesi
- **Minimum RTT (ms)**: En düşük Round Trip Time
- **Maksimum RTT (ms)**: En yüksek Round Trip Time
- **Ortalama RTT (ms)**: Ortalama Round Trip Time
- **Standart sapma (ms)**: RTT değerlerinin standart sapması (jitter)

## Örnek Kullanım Senaryoları

### Senaryo 1: İnternet Bağlantısı Kalitesi Testi

1. "Ping Testi" sekmesini açın
2. Hedef olarak "8.8.8.8" (Google DNS) girin
3. Ping Sayısı: 50
4. Zaman Aşımı: 2000 ms
5. Paket Boyutu: 56 bytes
6. Bekleme Süresi: 1000 ms
7. "Testi Başlat" butonuna tıklayın
8. Sonuçları değerlendirin:
   - %1'den az paket kaybı ve 50 ms altında ortalama RTT iyi bir bağlantıyı gösterir
   - Standart sapma 10 ms altında olmalı

### Senaryo 2: Yerel Ağ Performans Testi

1. "Ping Testi" sekmesini açın
2. Hedef olarak yerel ağ gateway'ini girin (örn. "192.168.1.1")
3. Ping Sayısı: 100
4. Zaman Aşımı: 500 ms
5. Paket Boyutu: 1472 bytes (tipik MTU değeri)
6. Bekleme Süresi: 100 ms
7. "Testi Başlat" butonuna tıklayın
8. Sonuçları değerlendirin:
   - Yerel ağda RTT değerlerinin 5 ms altında olması beklenir
   - Paket kaybı %0 olmalı
   - Standart sapma 1 ms altında olmalı

### Senaryo 3: Uzun Süreli Stabilite Testi

1. "Ping Testi" sekmesini açın
2. Hedef olarak izlemek istediğiniz sunucuyu girin
3. Ping Sayısı: 1000 (uzun gözlem için)
4. Zaman Aşımı: 2000 ms
5. Paket Boyutu: 56 bytes
6. Bekleme Süresi: 2000 ms
7. "Testi Başlat" butonuna tıklayın
8. Grafikte ani yükselmeler veya düşüşler, bağlantı kararsızlığını gösterir

## Sorun Giderme

### "Hostname Çözümlenemedi" Hatası

- Girilen alan adının doğru yazıldığından emin olun
- DNS sunucularınızla bağlantınızı kontrol edin
- Doğrudan IP adresi kullanmayı deneyin

### "Yanıt Alınamadı" veya Yüksek Paket Kaybı

- Firewall veya güvenlik yazılımlarının ICMP trafiğini engellemiyor olduğunu kontrol edin
- Ağ bağlantınızı kontrol edin
- Hedefe fiziksel ağ yolunda sorun olabilir

### Çok Yüksek RTT Değerleri

- İnternet bağlantınızın kalitesini kontrol edin
- Aynı ağda başka cihazlar tarafından yoğun bant genişliği kullanımını araştırın
- Daha yakın bir sunucuya ping atmayı deneyin

### "Erişim Reddedildi" Hatası

- Bazı ICMP paketleri için yönetici (admin) izinleri gerekebilir
- Programı yönetici olarak çalıştırmayı deneyin
