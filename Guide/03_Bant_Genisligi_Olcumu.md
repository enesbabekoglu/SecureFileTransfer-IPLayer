# Bant Genişliği Ölçümü Kılavuzu

Bu kılavuz, SecureFileTransfer-IPLayer projesindeki Bant Genişliği Ölçümü özelliklerini ayrıntılı şekilde açıklamaktadır. Bu modül, ağ bağlantınızın indirme ve yükleme hızlarını ölçmenize ve analiz etmenize olanak tanır.

## İçerik

1. [Genel Bakış](#genel-bakış)
2. [Arayüz Tanıtımı](#arayüz-tanıtımı)
3. [Ölçüm Parametreleri](#ölçüm-parametreleri)
4. [Test Türleri](#test-türleri)
5. [Sonuçları Yorumlama](#sonuçları-yorumlama)
6. [Grafik Görselleştirme](#grafik-görselleştirme)
7. [Örnek Kullanım Senaryoları](#örnek-kullanım-senaryoları)
8. [Sorun Giderme](#sorun-giderme)

## Genel Bakış

Bant Genişliği Ölçümü aracı, ağ bağlantınızın performansını ölçmenize olanak tanıyan güçlü bir araçtır. Bu araç ile:

- İndirme (download) hızınızı ölçebilirsiniz
- Yükleme (upload) hızınızı ölçebilirsiniz
- Zaman içindeki bant genişliği değişimlerini izleyebilirsiniz
- Ağ performansınızı çeşitli koşullar altında test edebilirsiniz
- Gerçek dünya verileriyle teorik bağlantı hızlarınızı karşılaştırabilirsiniz

## Arayüz Tanıtımı

Ağ Analiz aracının "Bant Genişliği Ölçümü" sekmesi aşağıdaki bölümlerden oluşur:

- **Test Sunucusu**: Bant genişliği testinin yapılacağı sunucu (varsayılan veya özel)
- **Test Türü**: İndirme, yükleme veya her ikisi için test seçeneği
- **Test Süresi**: Her test için ayrılan süre (saniye)
- **Veri Boyutu**: Transfer edilecek veri miktarı (MB)
- **Eşzamanlı Bağlantı**: Paralel bağlantı sayısı
- **Testi Başlat**: Bant genişliği testini başlatma butonu
- **Sonuç Alanı**: Test sonuçlarının gösterildiği metin alanı
- **Grafik Alanı**: Hız değerlerinin zaman içindeki değişiminin grafik gösterimi

## Ölçüm Parametreleri

### Test Sunucusu

- **Varsayılan Sunucular**: Sistem, otomatik olarak size yakın test sunucuları listesi sunar
- **Özel Sunucu**: İsterseniz kendi test sunucunuzun URL'sini belirtebilirsiniz
- **Sunucu Seçim Kriterleri**:
  - Ping süresi (düşük gecikme)
  - Coğrafi yakınlık
  - Sunucu yükü ve kullanılabilirliği

### Test Türü

- **İndirme Testi**: Sunucudan bilgisayarınıza veri transferi hızını ölçer
- **Yükleme Testi**: Bilgisayarınızdan sunucuya veri transferi hızını ölçer
- **Tam Test**: Hem indirme hem yükleme hızlarını sırayla ölçer

### Test Süresi

- **Aralık**: 5-120 saniye
- **Varsayılan**: 10 saniye
- **Öneriler**:
  - Hızlı test için: 5-10 saniye
  - Standart test için: 15-30 saniye
  - Detaylı test için: 60+ saniye

### Veri Boyutu

- **Aralık**: 1-1000 MB
- **Varsayılan**: Otomatik (bağlantı hızına göre ayarlanır)
- **Öneriler**:
  - Düşük bant genişliği bağlantıları için: 5-10 MB
  - Orta seviye bağlantılar için: 20-50 MB
  - Yüksek hızlı bağlantılar için: 100+ MB

### Eşzamanlı Bağlantı

- **Aralık**: 1-16
- **Varsayılan**: 4
- **Öneriler**:
  - Düşük bant genişliği için: 1-2 bağlantı
  - Normal evsel bağlantılar için: 3-5 bağlantı
  - Yüksek bant genişliği için: 6-10 bağlantı

## Test Türleri

### İndirme Testi

İndirme testi, veri sunucudan bilgisayarınıza ne kadar hızlı aktarılabileceğini ölçer:

1. Sistem, belirtilen test sunucusuna bağlanır
2. Sunucudan çeşitli boyutlarda veri blokları indirir
3. Transfer hızı, her saniye indirilen veri miktarı olarak hesaplanır
4. Test süresi boyunca veya belirtilen veri miktarı tamamlanana kadar devam eder
5. Maksimum, minimum ve ortalama indirme hızları raporlanır

### Yükleme Testi

Yükleme testi, verinin bilgisayarınızdan sunucuya ne kadar hızlı gönderilebileceğini ölçer:

1. Sistem, rastgele veri blokları oluşturur
2. Bu verileri belirtilen test sunucusuna gönderir
3. Transfer hızı, her saniye yüklenen veri miktarı olarak hesaplanır
4. Test süresi boyunca veya belirtilen veri miktarı tamamlanana kadar devam eder
5. Maksimum, minimum ve ortalama yükleme hızları raporlanır

### Tam Test

Tam test, sırasıyla indirme ve yükleme testlerini gerçekleştirir:

1. Önce indirme testi tamamlanır
2. Ardından kısa bir duraklama (2 saniye) sonrası yükleme testi başlar
3. Her iki testin sonuçları ayrı ayrı ve karşılaştırmalı olarak raporlanır

## Sonuçları Yorumlama

Bant genişliği testi sonuçları aşağıdaki metrikleri içerir:

### Hız Ölçümleri

- **Maximum Speed**: Ölçülen en yüksek hız değeri
- **Minimum Speed**: Ölçülen en düşük hız değeri
- **Average Speed**: Tüm ölçümlerin ortalaması
- **Current Speed**: Son ölçülen hız değeri

### Hız Birimleri

Sonuçlar iki farklı birimde gösterilir:
- **Mbps (Megabit per second)**: Saniyede megabit
- **MB/s (Megabyte per second)**: Saniyede megabayt (1 MB/s = 8 Mbps)

### Bağlantı Değerlendirmesi

Hız sonuçlarınıza göre bağlantı kalitesi otomatik olarak değerlendirilir:

- **Çok Düşük**: < 5 Mbps indirme, < 1 Mbps yükleme
- **Düşük**: 5-15 Mbps indirme, 1-3 Mbps yükleme
- **Orta**: 15-50 Mbps indirme, 3-10 Mbps yükleme
- **Yüksek**: 50-100 Mbps indirme, 10-20 Mbps yükleme
- **Çok Yüksek**: > 100 Mbps indirme, > 20 Mbps yükleme

## Grafik Görselleştirme

Bant genişliği testi sonuçları, zaman serisi grafiği olarak görselleştirilir:

- **X Ekseni**: Test süresi (saniye)
- **Y Ekseni**: Transfer hızı (Mbps)
- **Mavi Çizgi**: İndirme hızı
- **Yeşil Çizgi**: Yükleme hızı
- **Kırmızı Noktalı Çizgi**: Ortalama hız

### Grafik İşlevleri

- **Yakınlaştırma/Uzaklaştırma**: Fare tekerleği ile grafik üzerinde yakınlaştırma yapabilirsiniz
- **Kaydırma**: Grafik üzerinde sol tıklayarak sürükleme yapabilirsiniz
- **Anlık Değer Görüntüleme**: Grafik üzerindeki herhangi bir noktaya fare ile geldiğinizde tam değeri görebilirsiniz

### Grafik Kaydetme

Test sonuçlarını grafik olarak kaydedebilirsiniz:
- **PNG Formatı**: Yüksek kaliteli resim formatı
- **SVG Formatı**: Vektörel grafik formatı
- **CSV Verileri**: İleri analiz için ham veri

## Örnek Kullanım Senaryoları

### Senaryo 1: İnternet Servis Sağlayıcı (ISP) Performans Kontrolü

1. "Bant Genişliği Ölçümü" sekmesini açın
2. Test türü olarak "Tam Test" seçin
3. Test süresini 30 saniye olarak ayarlayın
4. Eşzamanlı bağlantı sayısını 5 olarak belirleyin
5. "Testi Başlat" butonuna tıklayın
6. Sonuçları ISP'nizin vaat ettiği hızlarla karşılaştırın:
   - Ölçülen hızlar, vaat edilen hızların en az %70-80'i olmalı
   - İndirme/yükleme oranları ISP'nin belirttiği oranlarla uyumlu olmalı

### Senaryo 2: Günün Farklı Saatlerinde Performans Testi

1. "Bant Genişliği Ölçümü" sekmesini açın
2. Test türü olarak "İndirme Testi" seçin
3. Aynı test sunucusunu kullanarak:
   - Sabah erken saatlerde (örn. 07:00)
   - Öğlen saatlerinde (örn. 13:00)
   - Akşam yoğun saatlerde (örn. 20:00)
   - Gece geç saatlerde (örn. 23:00)
4. Her test için sonuçları kaydedin ve karşılaştırın
5. Yoğun saatlerdeki performans düşüşlerini belirleyin

### Senaryo 3: Farklı Cihazların Karşılaştırılması

1. Aynı ağa bağlı farklı cihazlarda (bilgisayar, tablet, akıllı telefon) test yapın
2. Her cihaz için aynı parametreleri kullanın:
   - Aynı test sunucusu
   - 15 saniyelik test süresi
   - "Tam Test" seçeneği
3. Sonuçları karşılaştırın ve cihazlar arasındaki performans farklılıklarını belirleyin
4. Wi-Fi vs. Ethernet bağlantı türlerinin etkisini analiz edin

## Sorun Giderme

### "Sunucu Bağlantı Hatası"

- Seçilen test sunucusunun çalışır durumda olduğunu kontrol edin
- Farklı bir test sunucusu seçin
- İnternet bağlantınızın aktif olduğunu doğrulayın
- Güvenlik duvarı ayarlarınızı kontrol edin

### "Test Başlatılamadı" Hatası

- Ağ bağlantınızın aktif olduğunu kontrol edin
- Eşzamanlı bağlantı sayısını azaltın
- Uygulamayı yeniden başlatın
- Veri boyutunu azaltın

### Beklenenden Düşük Hızlar

- Ağda başka cihazların yüksek bant genişliği kullanımını kontrol edin
- Wi-Fi sinyal gücünü ve kalitesini kontrol edin (mümkünse kablolu bağlantı deneyin)
- Bilgisayarınızın kaynak kullanımını kontrol edin
- Farklı bir sunucu ile testi tekrarlayın
- Virüs taraması veya büyük güncellemelerin çalışmadığından emin olun
