# Ağ Koşulları Simülasyonu Kılavuzu

Bu kılavuz, SecureFileTransfer-IPLayer projesindeki Ağ Koşulları Simülasyonu özelliklerini ayrıntılı şekilde açıklamaktadır. Bu modül, çeşitli ağ koşullarını (gecikme, paket kaybı, jitter gibi) simüle etmenize olanak tanır.

## İçerik

1. [Genel Bakış](#genel-bakış)
2. [Arayüz Tanıtımı](#arayüz-tanıtımı)
3. [Simülasyon Parametreleri](#simülasyon-parametreleri)
4. [Önceden Tanımlanmış Senaryolar](#önceden-tanımlanmış-senaryolar)

## Genel Bakış

Ağ Koşulları Simülasyonu aracı, çeşitli ağ koşullarını kontrollü bir ortamda test etmenizi sağlar. Bu araç ile:

- Farklı gecikme (latency) değerlerini simüle edebilirsiniz
- Paket kaybı (packet loss) durumlarını test edebilirsiniz
- Jitter (gecikme değişkenliği) etkilerini gözlemleyebilirsiniz
- Bant genişliği kısıtlamalarını uygulayabilirsiniz
- Gerçek dünya ağ koşullarını laboratuvar ortamında yeniden oluşturabilirsiniz

## Arayüz Tanıtımı

Ağ Analiz aracının "Ağ Koşulları Simülasyonu" sekmesi aşağıdaki bölümlerden oluşur:

- **Gecikme (Latency)**: Ağ gecikmesi ekleme (ms cinsinden)
- **Paket Kaybı**: Rastgele paket kaybı oranı (% cinsinden)
- **Jitter**: Gecikme değişkenliği (ms cinsinden)
- **Bant Genişliği Kısıtlaması**: Maksimum bant genişliği (Kbps cinsinden)
- **Paket Yeniden Sıralaması**: Paketlerin sırasını değiştirme oranı
- **Senaryo Seçimi**: Önceden tanımlanmış ağ koşulu senaryoları
- **Hedef IP/Port**: Simülasyonun uygulanacağı hedef
- **Simülasyonu Başlat**: Seçilen parametrelerle simülasyonu başlatma butonu
- **Simülasyonu Durdur**: Aktif simülasyonu sonlandırma butonu
- **Sonuç Alanı**: Simülasyon durumu ve istatistiklerin gösterildiği alan

## Simülasyon Parametreleri

### Gecikme (Latency)

- **Aralık**: 0-5000 ms
- **Varsayılan**: 0 ms (gecikme yok)
- **Öneriler**:
  - Yerel ağ simülasyonu: 1-5 ms
  - Şehir içi bağlantı: 10-30 ms
  - Ülke içi bağlantı: 30-70 ms
  - Kıtalararası bağlantı: 100-300 ms
  - Uydu bağlantısı: 500-1000 ms

### Paket Kaybı

- **Aralık**: 0-100%
- **Varsayılan**: 0% (kayıp yok)
- **Öneriler**:
  - İyi kalitede bağlantı: 0-1%
  - Orta kalitede bağlantı: 1-5%
  - Kötü kalitede bağlantı: 5-15%
  - Çok kötü bağlantı: 15%+

### Jitter

- **Aralık**: 0-1000 ms
- **Varsayılan**: 0 ms (jitter yok)
- **Öneriler**:
  - Sabit bağlantı: 0-5 ms
  - Normal bağlantı: 5-20 ms
  - Yoğun bağlantı: 20-50 ms
  - Kablosuz/mobil bağlantı: 50-100 ms

### Bant Genişliği Kısıtlaması

- **Aralık**: 0-1000000 Kbps (0 = kısıtlama yok)
- **Varsayılan**: 0 Kbps (kısıtlama yok)
- **Öneriler**:
  - Dial-up bağlantı: 56 Kbps
  - ADSL: 1000-8000 Kbps
  - Fiber: 10000-100000 Kbps
  - 3G: 500-5000 Kbps
  - 4G: 5000-50000 Kbps
  - 5G: 50000-500000 Kbps

## Önceden Tanımlanmış Senaryolar

Sistem, hızlı test için aşağıdaki önceden tanımlanmış senaryoları içerir:

### Mükemmel Bağlantı
- Gecikme: 1 ms
- Paket Kaybı: 0%
- Jitter: 0 ms
- Bant Genişliği: Kısıtlama yok

### İyi Ev İnterneti
- Gecikme: 20 ms
- Paket Kaybı: 0.5%
- Jitter: 5 ms
- Bant Genişliği: 50000 Kbps

### 4G Mobil Bağlantı
- Gecikme: 50 ms
- Paket Kaybı: 1%
- Jitter: 20 ms
- Bant Genişliği: 20000 Kbps
