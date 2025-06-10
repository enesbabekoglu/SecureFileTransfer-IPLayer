# Güvenli Dosya Transferi - Sunucu Kullanım Kılavuzu

Bu kılavuz, SecureFileTransfer-IPLayer projesindeki Sunucu (Server) modülünün kullanımını ayrıntılı şekilde açıklamaktadır. Sunucu modülü, dosyaları güvenli bir şekilde saklamanıza ve istemcilerden gelen bağlantıları yönetmenize olanak tanır.

## İçerik

1. [Genel Bakış](#genel-bakış)
2. [Sunucu Arayüzü Tanıtımı](#sunucu-arayüzü-tanıtımı)
3. [Kurulum ve Başlatma](#kurulum-ve-başlatma)
4. [Bağlantıları Yönetme](#bağlantıları-yönetme)
5. [Dosya Alma ve Saklama](#dosya-alma-ve-saklama)
6. [Dosya Paylaşımı](#dosya-paylaşımı)
7. [Güvenlik Yapılandırması](#güvenlik-yapılandırması)
8. [Sorun Giderme](#sorun-giderme)

## Genel Bakış

Sunucu modülü, SecureFileTransfer sisteminin merkezi bileşenidir. Bu modül:

- Çoklu istemci bağlantılarını yönetir
- İstemcilerden gelen şifreli dosyaları alır ve saklar
- İstemcilere dosya listesi ve dosya içeriği sağlar
- Kimlik doğrulama ve yetkilendirme işlemlerini gerçekleştirir
- Dosya transferlerinin güvenliğini ve bütünlüğünü sağlar
- Sistem loglarını tutar ve raporlar

## Sunucu Arayüzü Tanıtımı

Sunucu arayüzü aşağıdaki bölümlerden oluşur:

- **Sunucu Durum Paneli**: Çalışma durumu ve temel istatistikler
- **Bağlantı Ayarları Paneli**: IP adresi ve port yapılandırması
- **Bağlantı Listesi**: Aktif istemci bağlantılarının listesi
- **Dosya Listesi**: Depolanan dosyaların listesi
- **Log Paneli**: Sistem logları ve aktivite kaydı
- **Güvenlik Ayarları**: Şifreleme ve kimlik doğrulama yapılandırması

### Kontroller ve Bileşenler

- **Sunucu Başlat/Durdur**: Sunucuyu çalıştırma ve durdurma düğmesi
- **Port**: Sunucunun dinleyeceği port numarası (varsayılan: 8000)
- **Dosya Dizini**: Dosyaların saklanacağı dizin seçimi
- **RSA Anahtar Seç**: Kimlik doğrulama için RSA anahtarı seçme düğmesi
- **Bağlantı Limiti**: Maksimum eşzamanlı bağlantı sayısı
- **İstemci Listesi**: Bağlı istemcilerin ve durumlarının listesi
- **Bağlantı Kes**: Seçili istemci bağlantısını kesme düğmesi
- **Log Kaydetme**: Sistem loglarını dosyaya kaydetme seçeneği
- **Temizle**: Log alanını temizleme düğmesi

## Kurulum ve Başlatma

### Sunucu Uygulamasını Başlatma

Sunucu uygulamasını başlatmak için:

1. Projenin ana dizininde terminali açın
2. Aşağıdaki komutu çalıştırın:
   ```
   python run_server.py
   ```
   veya
   ```
   python src/gui/app.py
   ```
   ve ana menüden "Server Mode"u seçin

3. Sunucu arayüzü başlatıldığında, bağlantı yapılandırma ekranı görüntülenir

### İlk Yapılandırma

Sunucuyu ilk kez çalıştırırken:

1. RSA anahtarı seçmeniz gerekir:
   - **RSA Anahtar Seç** düğmesine tıklayın
   - `keys` klasöründen `private_key.pem` dosyasını seçin
   - Anahtar dosyanız yoksa, önce `generate_keys.py` betiğini çalıştırarak anahtar oluşturmalısınız:
   ```
   python generate_keys.py
   ```

2. Bağlantı ayarlarını yapılandırın:
   - Port numarasını girin (varsayılan: 8000)
   - IP adresi otomatik olarak mevcut sistem IP adresini kullanır

3. Dosya depolama dizinini seçin:
   - Varsayılan olarak `./received_files` dizini kullanılır
   - Özel bir dizin seçmek için **Dosya Dizini** düğmesine tıklayın

4. Güvenlik ayarlarını yapılandırın:
   - Maksimum dosya boyutu (varsayılan: 1GB)
   - Parça boyutu (varsayılan: 4MB)
   - Şifreleme algoritması (varsayılan: AES-256-CFB)

5. **Sunucu Başlat** düğmesine tıklayın

## Bağlantıları Yönetme

### Bağlantı İzleme

Aktif istemci bağlantılarını izlemek için:

- **İstemci Listesi** panelini kontrol edin
- Burada her istemci için şu bilgiler görüntülenir:
  - İstemci IP adresi ve port numarası
  - Bağlantı zamanı
  - İstemci kimliği (client_id)
  - Aktarım durumu (aktif/beklemede)
  - Son aktivite

### Bağlantı Yönetimi

İstemci bağlantılarını yönetmek için:

1. Listeden bir istemci seçin
2. Aşağıdaki işlemleri gerçekleştirebilirsiniz:
   - **Detaylar**: İstemci hakkında detaylı bilgi görüntüleme
   - **Bağlantı Kes**: Seçili istemcinin bağlantısını kesme
   - **Mesaj Gönder**: İstemciye bildirim mesajı gönderme
   - **İzinler**: İstemcinin dosya erişim izinlerini yönetme

### Bağlantı Limitleri

Sunucu performansını korumak için:

- Maksimum eş zamanlı bağlantı sayısını ayarlayın (önerilen: 10-20)
- Yüksek ağ yükü durumunda limit değerini düşürün
- Her istemci için maksimum aktarım hızını ayarlayabilirsiniz
- Uzun süre pasif kalan bağlantılar için zaman aşımı değerini ayarlayın

## Dosya Alma ve Saklama

### Dosya Alımı

Sunucu, istemcilerden dosyaları şu şekilde alır:

1. İstemci, dosya gönderme isteği başlatır
2. Sunucu, dosya metadatalarını kontrol eder (boyut, isim, hash)
3. Sunucu, depolama alanını kontrol eder ve yeterli alan varsa onay verir
4. İstemci, şifreli dosya parçalarını gönderir
5. Sunucu, her parçayı alır ve geçici bir konumda saklar
6. Tüm parçalar alındığında bütünlük doğrulaması yapılır
7. Doğrulama başarılıysa dosya kalıcı depolama konumuna taşınır

### Dosya Saklama

Dosyalar aşağıdaki yapıda saklanır:

```
/received_files
    ├── user1_id/
    │   ├── file1.txt
    │   └── file2.pdf
    └── user2_id/
        ├── file3.docx
        └── file4.jpg
```

Her istemci için ayrı bir klasör oluşturulur ve dosyalar bu klasör altında saklanır. Bu yapı:

- Kullanıcılar arası dosya izolasyonu sağlar
- Erişim kontrolünü kolaylaştırır
- Kullanıcı bazında kotaların yönetilmesini sağlar

### Depolama Yönetimi

Sunucu depolama alanını yönetmek için:

1. **Depolama Bilgisi** düğmesine tıklayın
2. Aşağıdaki bilgiler görüntülenecektir:
   - Toplam kullanılan alan
   - Her kullanıcının kullandığı alan
   - Kalan boş alan
   - En büyük dosyalar
3. **Temizleme Seçenekleri** ile eski veya büyük dosyaları yönetebilirsiniz

## Dosya Paylaşımı

### Dosya Listesini Görüntüleme

Sunucudaki dosyaları görüntülemek için:

1. **Dosya Listesi** sekmesine gidin
2. Tüm dosyalar veya kullanıcı bazında filtrelenmiş liste görüntülenir
3. Her dosya için şu bilgiler gösterilir:
   - Dosya adı ve uzantısı
   - Boyut
   - Yükleme tarihi
   - Sahip olan kullanıcı
   - Hash değeri

### Dosya Erişim Kontrolü

Dosya erişimini yönetmek için:

1. **Dosya Listesi** sekmesinde bir dosya seçin
2. **Erişim Kontrolü** düğmesine tıklayın
3. Aşağıdaki erişim ayarlarını yapabilirsiniz:
   - Tüm kullanıcılar için erişim
   - Belirli kullanıcılar için erişim
   - Erişim için şifre tanımlama
   - Geçici erişim süresi belirleme

### Dosya İşlemleri

Sunucudaki dosyalar üzerinde şu işlemleri gerçekleştirebilirsiniz:

- **Sil**: Seçili dosyayı sunucudan silme
- **Yeniden Adlandır**: Dosyayı yeniden adlandırma
- **Taşı**: Dosyayı farklı bir kullanıcı klasörüne taşıma
- **Detaylar**: Dosya hakkında detaylı bilgileri görüntüleme
- **Log**: Dosya ile ilgili tüm işlem geçmişini görüntüleme

## Güvenlik Yapılandırması

### RSA Anahtar Yönetimi

Sunucu kimlik doğrulaması için:

1. **Güvenlik Ayarları** sekmesine gidin
2. **RSA Anahtar Yönetimi** bölümünü seçin
3. Mevcut anahtarı görüntüleyin veya yeni anahtar oluşturun
4. Genel anahtarı dışa aktarın (istemciler için)
5. Anahtar rotasyonu için zaman aralığını ayarlayın

### Şifreleme Ayarları

Veri şifreleme parametrelerini yapılandırmak için:

1. **Güvenlik Ayarları** sekmesine gidin
2. **Şifreleme Yapılandırması** bölümünü seçin
3. Şu parametreleri ayarlayabilirsiniz:
   - AES anahtar boyutu (128, 192, 256 bit)
   - IV (Başlatma Vektörü) oluşturma yöntemi
   - Hash algoritması (SHA-256, SHA-384, SHA-512)

### Kimlik Doğrulama Ayarları

Kimlik doğrulama mekanizmalarını yapılandırmak için:

1. **Güvenlik Ayarları** sekmesine gidin
2. **Kimlik Doğrulama Yapılandırması** bölümünü seçin
3. Şu parametreleri ayarlayabilirsiniz:
   - Oturum token süresi
   - Maksimum başarısız giriş denemesi
   - Güvenilen istemciler listesi
   - İzin verilen IP adresleri aralığı

## Sorun Giderme

### "Sunucu Başlatılamadı" Hatası

- Port numarasının başka bir uygulama tarafından kullanılmadığını kontrol edin
- Yönetici (admin) izinlerine sahip olduğunuzdan emin olun
- Güvenlik duvarı izinlerini kontrol edin
- Farklı bir port numarası ile deneyin

### "RSA Anahtarı Yüklenemedi" Hatası

- Doğru özel anahtar dosyasını seçtiğinizi kontrol edin
- Anahtar dosyasının bozulmadığından emin olun
- Erişim izinlerini kontrol edin
- Gerekirse yeni bir anahtar çifti oluşturun

### "Disk Alanı Yetersiz" Uyarısı

- Mevcut disk alanını kontrol edin
- Gereksiz dosyaları temizleyin
- Dosya saklama konumunu daha fazla alana sahip bir diske değiştirin
- Kullanıcı bazında kota tanımlayın

### "İstemci Bağlantı Hatası" Mesajı

- Ağ bağlantısını kontrol edin
- Sunucunun erişilebilir olduğundan emin olun
- Maksimum bağlantı sayısının aşılmadığını kontrol edin
- İstemcinin geçerli bir RSA anahtarı kullandığını doğrulayın
