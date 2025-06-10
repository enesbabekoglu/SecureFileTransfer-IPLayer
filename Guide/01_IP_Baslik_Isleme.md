# IP Başlık İşleme Kılavuzu

Bu kılavuz, SecureFileTransfer-IPLayer projesindeki IP Başlık İşleme özelliklerini ayrıntılı şekilde açıklamaktadır. Bu modül, IP paketlerini oluşturma, analiz etme ve manipüle etme işlemlerini gerçekleştirmenize olanak tanır.

## İçerik

1. [Genel Bakış](#genel-bakış)
2. [Arayüz Tanıtımı](#arayüz-tanıtımı)
3. [IP Başlık Alanları](#ip-başlık-alanları)
4. [Paket Oluşturma](#paket-oluşturma)
5. [Checksum Hesaplama](#checksum-hesaplama)
6. [Paket Parçalama (Fragmentation)](#paket-parçalama-fragmentation)
7. [Paket Bilgilerini Görüntüleme](#paket-bilgilerini-görüntüleme)
8. [Örnek Kullanım Senaryoları](#örnek-kullanım-senaryoları)
9. [Sorun Giderme](#sorun-giderme)

## Genel Bakış

IP Başlık İşleme aracı, IP protokolünün düşük seviyeli işleyişini anlamanıza, özel IP paketleri oluşturmanıza ve manipüle etmenize yardımcı olmak için tasarlanmıştır. Bu araç, ağ güvenliği testleri, protokol incelemesi veya ağ analizleri için kullanılabilir.

## Arayüz Tanıtımı

Ağ Analiz aracının "IP Başlık İşleme" sekmesi aşağıdaki bölümlerden oluşur:

- **Hedef IP**: Paketin gönderileceği hedef IP adresi
- **Kaynak IP**: Paketin kaynağı olarak görünecek IP adresi (opsiyonel)
- **TTL (Time to Live)**: Paketin ağda yaşayacağı maksimum router sayısı
- **Protokol**: Taşınan verinin protokolü (TCP, UDP, ICMP vb.)
- **Paket Boyutu**: Paketin içinde taşınacak veri boyutu
- **Paket Oluştur**: Belirtilen parametrelerle paket oluşturma butonu
- **Checksum Hesapla**: Oluşturulan paketin checksum değerini hesaplama butonu
- **Paketi Parçala**: Büyük paketleri belirtilen boyutlarda parçalama butonu
- **Paket Bilgisini Göster**: Oluşturulan paketin içeriğini detaylı gösterme butonu

## IP Başlık Alanları

IP başlığı aşağıdaki alanlardan oluşur:

| Alan | Boyut (bit) | Açıklama |
|------|-------------|----------|
| Versiyon | 4 | IP protokolünün versiyonu (IPv4 için 4) |
| IHL (Internet Header Length) | 4 | IP başlığının uzunluğu (32-bit word cinsinden) |
| DSCP (Differentiated Services Code Point) | 6 | QoS için kullanılan öncelik değeri |
| ECN (Explicit Congestion Notification) | 2 | Tıkanıklık bildirimi |
| Toplam Uzunluk | 16 | Paketin toplam boyutu (başlık + veri) |
| Kimlik (Identification) | 16 | Paket parçalarını birleştirmek için kimlik numarası |
| Bayraklar (Flags) | 3 | Parçalama kontrolü için bayraklar |
| Fragment Offset | 13 | Parça içindeki veri konumu |
| TTL (Time To Live) | 8 | Paketin maksimum yaşam süresi |
| Protokol | 8 | Taşınan verinin protokolü (TCP=6, UDP=17, ICMP=1 vb.) |
| Başlık Sağlama Toplamı (Checksum) | 16 | Başlık bütünlüğünü kontrol için sağlama toplamı |
| Kaynak IP | 32 | Paketin kaynağı |
| Hedef IP | 32 | Paketin varış noktası |
| Seçenekler (Options) | Değişken | Opsiyonel başlık alanları |

## Paket Oluşturma

IP paketi oluşturmak için:

1. Ağ Analiz aracından "IP Başlık İşleme" sekmesini açın
2. Hedef IP alanına geçerli bir IPv4 adresi girin (örn. "8.8.8.8")
3. İsterseniz Kaynak IP alanını doldurun (boş bırakılırsa mevcut makinenin IP'si kullanılır)
4. TTL değerini ayarlayın (1-255 arası değer, varsayılan 64)
5. Protokol değerini seçin (TCP için 6, UDP için 17, ICMP için 1)
6. Paket boyutu için istediğiniz değeri girin (20-65535 arası)
7. "Paket Oluştur" butonuna tıklayın

Bu işlem, belirttiğiniz parametrelerle bir IP paketi oluşturacak ve sonuçları ekranda gösterecektir.

## Checksum Hesaplama

IP başlık sağlama toplamı (checksum), başlık verilerinin bütünlüğünü doğrulamak için kullanılan 16-bitlik bir değerdir.

Checksum hesaplamak için:

1. Önce bir IP paketi oluşturun
2. "Checksum Hesapla" butonuna tıklayın
3. Hesaplanan checksum değeri ve doğrulama sonucu ekranda görüntülenecektir

Checksum hesaplama algoritması:
- Başlığın tüm 16-bit word'leri toplanır
- Taşma bitlerini tekrar toplama ekleyerek 16-bitte tutar
- Son değerin 1'e tümleyeni alınır

## Paket Parçalama (Fragmentation)

Büyük IP paketleri, ağ geçidi MTU (Maximum Transmission Unit) değerlerinden büyükse parçalanmalıdır.

Paketi parçalamak için:

1. Önce büyük bir IP paketi oluşturun (örn. boyutu 1500+ byte)
2. "Paketi Parçala" butonuna tıklayın
3. Açılan pencerede parça boyutu girin (örn. 576 veya 1280 byte)
4. "Parçala" butonuna tıklayın

Sistem, paketi belirtilen boyuttaki parçalara ayıracak ve her parça için:
- Fragment offset değeri ayarlanır
- More fragments bayrağı uygun şekilde ayarlanır (son parça hariç)
- Her parçanın başlık checksum'ı yeniden hesaplanır

## Paket Bilgilerini Görüntüleme

Oluşturulan veya parçalanan paketlerin detaylarını görmek için:

1. "Paket Bilgisini Göster" butonuna tıklayın
2. Paket bilgileri aşağıdaki detaylarla birlikte görüntülenecektir:
   - Tüm başlık alanları ve değerleri
   - Hexadecimal formatında başlık dump'ı
   - Checksum doğrulama sonucu
   - Toplam paket boyutu

## Örnek Kullanım Senaryoları

### Senaryo 1: Özel IP Paketi Oluşturma ve İnceleme

1. "IP Başlık İşleme" sekmesini açın
2. Hedef IP: 192.168.1.1
3. Kaynak IP: 10.0.0.1
4. TTL: 30
5. Protokol: 17 (UDP)
6. Paket Boyutu: 1000
7. "Paket Oluştur" butonuna tıklayın
8. "Paket Bilgisini Göster" ile detayları inceleyin

### Senaryo 2: MTU Problemlerini Simüle Etme

1. "IP Başlık İşleme" sekmesini açın
2. Büyük bir paket oluşturun (örn. 2000 byte)
3. "Paketi Parçala" butonuna tıklayarak 576 byte parçalara ayırın
4. Oluşan parçaların Fragment Offset ve More Fragments bayraklarının doğru ayarlandığını kontrol edin

### Senaryo 3: Checksum Doğrulama Testi

1. Bir IP paketi oluşturun
2. "Checksum Hesapla" ile sağlama toplamını hesaplayın
3. Manuel olarak başlık verilerini değiştirin (başlık alanlarını düzenleyin)
4. Tekrar "Checksum Hesapla" ile sağlama toplamını kontrol edin
5. Değişiklikten sonra checksum'ın geçersiz olduğunu gözlemleyin

## Sorun Giderme

### "Geçersiz IP Adresi" Hatası

- IP adresinin doğru formatta olduğundan emin olun (örn. "192.168.1.1")
- Geçersiz karakterler veya aralıklar içermediğini kontrol edin

### "Checksum Doğrulaması Başarısız" Uyarısı

- Başlık değerlerinin manipüle edilmiş olabilir
- Paket bütünlüğü bozulmuş olabilir
- "Paket Oluştur" ile yeni bir paket oluşturun

### "Parçalama Başarısız" Hatası

- Parça boyutunun minimum IP başlık boyutundan (20 byte) büyük olduğundan emin olun
- Parça boyutunun 8'in katı olduğundan emin olun (offset hesaplaması için)
- Toplam boyutun geçerli bir değer olduğunu kontrol edin (65535 byte'dan küçük)
