# MITM (Man-in-the-Middle) Saldırı Simülasyonu Kılavuzu

Bu kılavuz, SecureFileTransfer-IPLayer projesindeki MITM Saldırı Simülasyonu özelliklerini ayrıntılı şekilde açıklamaktadır. Bu modül, ortadaki adam saldırılarını simüle etmenize ve güvenlik önlemlerinizi test etmenize olanak tanır.

## İçerik

1. [Genel Bakış](#genel-bakış)
2. [Arayüz Tanıtımı](#arayüz-tanıtımı)
3. [MITM Saldırı Türleri](#mitm-saldırı-türleri)
4. [Simülasyon Parametreleri](#simülasyon-parametreleri)
5. [Güvenlik Testleri](#güvenlik-testleri)
6. [Sonuçları Yorumlama](#sonuçları-yorumlama)
7. [Önlemler ve İyileştirmeler](#önlemler-ve-iyileştirmeler)

## Genel Bakış

MITM (Man-in-the-Middle) Saldırı Simülasyonu aracı, güvenli veri iletişiminin saldırılara karşı test edilmesi için tasarlanmıştır. Bu araç ile:

- İki taraf arasındaki iletişimi yakalayabilirsiniz
- Aktarılan verileri görüntüleyebilirsiniz
- Şifreleme ve kimlik doğrulama mekanizmalarını test edebilirsiniz
- Güvenlik açıklarını tespit edebilirsiniz
- Güvenlik önlemlerinizin etkinliğini değerlendirebilirsiniz

Bu aracın amacı, sadece eğitim ve güvenlik testi amacıyla kullanılmasıdır. Başkalarının veri iletişimini izlemek için kullanılması yasal ve etik değildir.

## Arayüz Tanıtımı

MITM Simülasyonu aracı aşağıdaki bölümlerden oluşur:

- **Saldırı Türü**: Uygulanacak MITM saldırı türü seçimi
- **Hedef IP/Port**: İzlenecek hedefin IP adresi ve port numarası
- **Kaynak IP/Port**: İzlenecek kaynağın IP adresi ve port numarası
- **Ağ Arabirimi**: Simülasyon için kullanılacak ağ kartı seçimi
- **Saldırıyı Başlat**: Simülasyon saldırısını başlatma butonu
- **Saldırıyı Durdur**: Aktif simülasyonu sonlandırma butonu
- **Yakalanan Trafik**: Yakalanan paketlerin gösterildiği alan
- **Veri İçeriği**: Yakalanan verilerin içeriği (şifrelenmiş/şifresiz)
- **Rapor**: Test sonuçlarının ve güvenlik değerlendirmesinin gösterildiği alan

## MITM Saldırı Türleri

### 1. ARP Zehirlemesi (ARP Poisoning)

- **Açıklama**: Yerel ağda ARP protokolünün zayıflığını kullanarak hedeflerin MAC adreslerini yanıltır
- **Çalışma Prensibi**: 
  1. Saldırgan, ağ geçidine kurbanın MAC adresi olarak kendi MAC adresini bildirir
  2. Kurbana ise ağ geçidinin MAC adresi olarak kendi MAC adresini bildirir
  3. Böylece tüm trafik saldırgan üzerinden geçer
- **Uygulanabilirlik**: Aynı yerel ağdaki cihazlar üzerinde etkilidir

### 2. DNS Önbellek Zehirlemesi (DNS Spoofing)

- **Açıklama**: DNS sorguları yanıtlanarak hedefin sahte web sitelerine yönlendirilmesi
- **Çalışma Prensibi**: 
  1. Saldırgan, hedefin DNS sorgularını yakalar
  2. Gerçek DNS sunucusundan önce sahte yanıtlar göndererek hedefi yönlendirir
  3. Hedef, gerçek site yerine saldırganın sahte sitesine bağlanır
- **Uygulanabilirlik**: DNS trafiği şifresiz olduğunda etkilidir

### 3. SSL/TLS Araya Girme (SSL Interception)

- **Açıklama**: HTTPS trafiğini ele geçirmek için "sahte" SSL sertifikaları kullanılır
- **Çalışma Prensibi**: 
  1. Saldırgan, kendi oluşturduğu sertifikayı kullanarak aradaki şifreli trafiği çözer
  2. Veriyi görüntüler veya değiştirir
  3. Tekrar şifreleyerek hedefe iletir
- **Uygulanabilirlik**: Sertifika doğrulaması yapılmadığında etkilidir

### 4. Wi-Fi Tuzak Ağı (Evil Twin)

- **Açıklama**: Gerçek bir Wi-Fi ağına benzer bir sahte ağ oluşturma
- **Çalışma Prensibi**: 
  1. Saldırgan, bilinen bir Wi-Fi ağı ile aynı SSID'ye sahip sahte bir ağ oluşturur
  2. Kurban bu sahte ağa bağlandığında, tüm trafiği saldırgan üzerinden geçer
- **Uygulanabilirlik**: Açık Wi-Fi ağlarında ve güvenlik farkındalığı düşük kullanıcılarda etkilidir

## Simülasyon Parametreleri

### Saldırı Türü Seçimi

- **ARP Zehirlemesi**: Yerel ağda kullanılan en yaygın MITM yöntemi
- **DNS Önbellek Zehirlemesi**: Belirli domainlere yönelik saldırılar için
- **SSL/TLS Araya Girme**: HTTPS trafiğini analiz etmek için
- **Wi-Fi Tuzak Ağı**: Kablosuz ağlarda kullanıcıları tuzağa düşürmek için

### Hedef Seçimi

- **Tek Hedef Modu**: Belirli bir IP veya MAC adresine yönelik saldırı
- **Ağ Modu**: Belirtilen alt ağdaki (subnet) tüm cihazlara yönelik saldırı
- **Seçici Mod**: Belirli protokolleri (HTTP, SMTP, FTP vb.) kullanan trafiğin hedeflenmesi

### Filtreleme Seçenekleri

- **Protokol Filtresi**: Sadece belirli protokolleri (HTTP, HTTPS, FTP vb.) yakalar
- **Port Filtresi**: Belirli portlara yönelik trafiği yakalar
- **İçerik Filtresi**: Belirli anahtar kelimeleri içeren paketleri yakalar

## Güvenlik Testleri

MITM saldırı simülasyonu ile aşağıdaki güvenlik testleri gerçekleştirilebilir:

### 1. Şifreleme Testi

- **Amaç**: Veri transferi sırasında şifrelemenin etkinliğini test etmek
- **Prosedür**:
  1. İstemci ve sunucu arasında veri transferi başlatın
  2. MITM saldırısını aktifleştirin
  3. Yakalanan verilerin şifreli olup olmadığını kontrol edin
  4. Şifreleme algoritmasının gücünü değerlendirin
- **Beklenen Sonuç**: Veriler şifreliyse ve çözülemiyorsa, şifreleme güvenlidir

### 2. Kimlik Doğrulama Testi

- **Amaç**: Kimlik doğrulama mekanizmalarının güvenliğini test etmek
- **Prosedür**:
  1. MITM saldırısını aktifleştirin
  2. İstemci sunucuya kimlik doğrulaması yapmaya çalışsın
  3. Kimlik bilgilerinin yakalanıp yakalanamadığını kontrol edin
- **Beklenen Sonuç**: Kimlik bilgileri şifreli olmalı veya yakalanamamalı

### 3. Sertifika Doğrulama Testi

- **Amaç**: SSL/TLS sertifika doğrulama mekanizmalarını test etmek
- **Prosedür**:
  1. SSL/TLS araya girme saldırısını başlatın
  2. İstemcinin sahte sertifikayı kabul edip etmediğini gözlemleyin
- **Beklenen Sonuç**: İstemci, sahte sertifikayı reddetmeli ve bağlantıyı sonlandırmalı

### 4. Protokol Güvenliği Testi

- **Amaç**: Kullanılan protokollerin güvenliğini değerlendirmek
- **Prosedür**:
  1. MITM saldırısını aktifleştirin
  2. Farklı protokollerdeki (HTTP, HTTPS, FTP, SSH vb.) trafiği yakalamayı deneyin
- **Beklenen Sonuç**: Güvenli protokoller (HTTPS, SSH) korunurken, güvensiz protokoller (HTTP, FTP) riske açık olabilir

## Sonuçları Yorumlama

Simülasyon sonuçları şu bilgileri içerir:

### Yakalanan Paket Analizi

- **Protokol Dağılımı**: Hangi protokollerin ne oranda kullanıldığı
- **Şifrelenmiş vs. Şifresiz**: Şifreli ve şifresiz veri oranı
- **Hassas Veri**: Yakalanan hassas bilgiler (şifreler, token'lar vb.)

### Güvenlik Raporu

- **Risk Seviyesi**: Düşük, Orta, Yüksek, Kritik
- **Tespit Edilen Açıklar**: Bulunan güvenlik açıkları ve potansiyel etkileri
- **İyileştirme Önerileri**: Güvenliği artırmak için öneriler

## Önlemler ve İyileştirmeler

### ARP Zehirlemesine Karşı

- Statik ARP tabloları kullanın
- ARP izleme yazılımları kurun
- Port güvenliği ve MAC filtreleme uygulayın

### DNS Saldırılarına Karşı

- DNSSEC kullanın
- DNS trafiğini şifreleyin (DoH, DoT)
- DNS önbelleğini düzenli olarak temizleyin

### SSL/TLS Araya Girme Saldırılarına Karşı

- Sertifika sabitlemesi (Certificate Pinning) kullanın
- HSTS (HTTP Strict Transport Security) uygulayın
- Kullanıcıları sertifika uyarıları konusunda eğitin

### Genel Güvenlik Önlemleri

- End-to-end şifreleme kullanın
- Güvenli protokoller tercih edin (HTTPS, SFTP, SSH)
- Düzenli güvenlik denetimleri ve testleri yapın
