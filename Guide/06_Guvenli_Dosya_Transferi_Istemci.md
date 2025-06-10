# Güvenli Dosya Transferi - İstemci Kullanım Kılavuzu

Bu kılavuz, SecureFileTransfer-IPLayer projesindeki İstemci (Client) modülünün kullanımını ayrıntılı şekilde açıklamaktadır. İstemci modülü, dosyaları güvenli bir şekilde uzak sunucuya aktarmanıza olanak tanır.

## İçerik

1. [Genel Bakış](#genel-bakış)
2. [İstemci Arayüzü Tanıtımı](#istemci-arayüzü-tanıtımı)
3. [Kurulum ve Başlatma](#kurulum-ve-başlatma)
4. [Sunucuya Bağlanma](#sunucuya-bağlanma)
5. [Dosya Gönderme](#dosya-gönderme)
6. [Dosya Alma](#dosya-alma)
7. [Güvenlik Özellikleri](#güvenlik-özellikleri)
8. [Sorun Giderme](#sorun-giderme)

## Genel Bakış

İstemci modülü, SecureFileTransfer sisteminin kullanıcı tarafındaki bileşenidir. Bu modül:

- Güvenli dosya transferi için sunucuya bağlanır
- Dosyaları AES-CFB şifrelemesi ile şifreler
- Dosyaları parçalara (chunk) böler ve SHA-256 hash'lerini hesaplar
- Şifreli dosya parçalarını sunucuya gönderir
- Sunucudan şifreli dosya parçalarını alır ve şifresini çözer
- Dosya bütünlüğünü doğrular
- Kullanıcı dostu bir grafik arayüzü sunar

## İstemci Arayüzü Tanıtımı

İstemci arayüzü aşağıdaki bölümlerden oluşur:

- **Bağlantı Ayarları Paneli**: Sunucu IP adresi ve port numarası girişi
- **Dosya İşlemleri Paneli**: Dosya seçimi ve aktarım kontrolleri
- **Log Paneli**: İşlem durumlarını gösteren log alanı
- **Şifreleme Ayarları Paneli**: Anahtar yönetimi ve şifreleme parametreleri
- **Durum Çubuğu**: Bağlantı durumu ve aktarım bilgileri

### Kontroller ve Bileşenler

- **Sunucu IP**: Bağlanılacak sunucunun IPv4 adresi
- **Port**: Sunucu port numarası (varsayılan: 8000)
- **Bağlan/Bağlantıyı Kes**: Sunucuya bağlantı kurma/kesme düğmesi
- **Dosya Seç**: Göndermek istediğiniz dosyayı seçme düğmesi
- **Gönder**: Seçili dosyayı sunucuya gönderme düğmesi
- **Dosyaları Listele**: Sunucudaki mevcut dosyaları listeleme düğmesi
- **İndir**: Sunucudan seçili dosyayı indirme düğmesi
- **RSA Anahtar Seç**: Kimlik doğrulama için RSA anahtarı seçme düğmesi
- **Temizle**: Log alanını temizleme düğmesi

## Kurulum ve Başlatma

### İstemci Uygulamasını Başlatma

İstemci uygulamasını başlatmak için:

1. Projenin ana dizininde terminali açın
2. Aşağıdaki komutu çalıştırın:
   ```
   python run_client.py
   ```
   veya
   ```
   python src/gui/app.py
   ```
   ve ana menüden "Client Mode"u seçin

3. İstemci arayüzü başlatıldığında, bağlantı yapılandırma ekranı görüntülenir

### İlk Yapılandırma

İstemciyi ilk kez çalıştırırken:

1. RSA anahtarı seçmeniz gerekir:
   - **RSA Anahtar Seç** düğmesine tıklayın
   - `keys` klasöründen `private_key.pem` dosyasını seçin
   - Anahtar dosyanız yoksa, önce `generate_keys.py` betiğini çalıştırarak anahtar oluşturmalısınız:
   ```
   python generate_keys.py
   ```

2. Bağlantı ayarlarını yapılandırın:
   - Sunucu IP adresini ve port numarasını girin
   - Varsayılan port: 8000

## Sunucuya Bağlanma

Sunucuya bağlanmak için:

1. Sunucu IP adresi ve port numarasını doğru girin
2. RSA anahtarınızı seçtiğinizden emin olun
3. **Bağlan** düğmesine tıklayın
4. Bağlantı başarılı olursa, durum çubuğu "Bağlandı" olarak güncellenir
5. Bağlantı başarısız olursa, hata mesajı log alanında görüntülenir

### Bağlantı Güvenliği

İstemci-sunucu bağlantısı aşağıdaki adımlarla güvence altına alınır:

1. RSA anahtarları kullanılarak kimlik doğrulama yapılır
2. İstemci, sunucuya genel anahtarını gönderir
3. Sunucu, istemcinin kimliğini doğrular
4. Oturum için bir token oluşturulur ve bu token tüm sonraki işlemler için kullanılır

## Dosya Gönderme

Sunucuya dosya göndermek için:

1. **Dosya Seç** düğmesine tıklayın ve göndermek istediğiniz dosyayı seçin
2. Seçilen dosyanın adı ve boyutu arayüzde görüntülenir
3. **Gönder** düğmesine tıklayın
4. Aktarım sırasında ilerleme çubuğu güncellenir
5. Aktarım tamamlandığında başarı mesajı görüntülenir

### Dosya Gönderme Aşamaları

Dosya gönderme süreci aşağıdaki aşamalardan oluşur:

1. **Hazırlık**: Dosya okunur ve metadataları hazırlanır
2. **Parçalama**: Dosya yapılandırılmış boyuttaki parçalara bölünür (varsayılan: 4 MB)
3. **Şifreleme**: Her parça AES-CFB algoritması ile şifrelenir
4. **Hash Hesaplama**: Her parçanın SHA-256 hash değeri hesaplanır
5. **AES Anahtarı Şifreleme**: AES anahtarı, sunucunun RSA genel anahtarı ile şifrelenir
6. **Transfer**: Şifreli parçalar ve metaveriler sunucuya gönderilir
7. **Doğrulama**: Sunucudan gelen parça alındı onayları kontrol edilir

## Dosya Alma

Sunucudan dosya almak için:

1. **Dosyaları Listele** düğmesine tıklayarak sunucudaki dosyaları görüntüleyin
2. Listeden indirmek istediğiniz dosyayı seçin
3. **İndir** düğmesine tıklayın
4. İndirme konumunu seçin
5. İndirme işlemi başlar ve ilerleme çubuğu güncellenir
6. İndirme tamamlandığında başarı mesajı görüntülenir

### Dosya Alma Aşamaları

Dosya alma süreci aşağıdaki aşamalardan oluşur:

1. **Dosya Bilgisi Alma**: Sunucudan seçilen dosyanın metadataları alınır
2. **AES Anahtarı Alma**: Şifreli AES anahtarı alınır ve istemcinin RSA özel anahtarı ile çözülür
3. **Parça İndirme**: Şifreli dosya parçaları indirilir
4. **Şifre Çözme**: Parçaların şifresi AES anahtarı ile çözülür
5. **Hash Doğrulama**: Her parçanın hash değeri kontrol edilir
6. **Birleştirme**: Parçalar orijinal dosyayı oluşturmak üzere birleştirilir

## Güvenlik Özellikleri

### Şifreleme Mekanizmaları

- **AES-CFB Şifreleme**: Dosya içeriği için 256-bit AES-CFB modu kullanılır
- **RSA-OAEP Şifreleme**: AES anahtarlarının güvenli aktarımı için kullanılır
- **SHA-256 Hash**: Dosya bütünlüğünü doğrulamak için kullanılır

### Kimlik Doğrulama

- **RSA Anahtar Çifti**: Her istemci ve sunucu, benzersiz RSA anahtar çiftlerine sahiptir
- **Token Tabanlı Oturum**: Başarılı kimlik doğrulamasından sonra, tüm işlemler için güvenli token kullanılır

### Bütünlük Kontrolleri

- **Parça Hash Doğrulaması**: Her dosya parçası için SHA-256 hash değerleri karşılaştırılır
- **Transfer Doğrulama**: Aktarılan her parça için onay mekanizması bulunur
- **Bütünlük Raporu**: Transfer sonunda genel bir bütünlük raporu oluşturulur

## Sorun Giderme

### "Sunucuya Bağlanılamadı" Hatası

- Sunucu IP adresinin doğru olduğunu kontrol edin
- Sunucunun çalışır durumda olduğundan emin olun
- Port numarasının doğru olduğunu kontrol edin
- Ağ bağlantınızı kontrol edin
- Güvenlik duvarı ayarlarınızı kontrol edin

### "RSA Anahtarı Yüklenemedi" Hatası

- Doğru özel anahtar dosyasını seçtiğinizi kontrol edin
- Anahtar dosyasının bozulmadığından emin olun
- Erişim izinlerini kontrol edin
- Gerekirse yeni bir anahtar çifti oluşturun

### "Dosya Gönderilemedi" Hatası

- Sunucu bağlantısının hala aktif olduğunu kontrol edin
- Dosyanın erişilebilir olduğundan emin olun
- Sunucuda yeterli depolama alanı olduğunu kontrol edin
- Ağ bağlantısının kararlı olduğunu kontrol edin

### "Dosya İndirilemedi" Hatası

- Dosyanın sunucuda mevcut olduğunu kontrol edin
- İndirme konumunda yazma iznine sahip olduğunuzu kontrol edin
- Depolama alanınızın yeterli olduğunu kontrol edin

### "Şifre Çözme Hatası" Mesajı

- Doğru RSA anahtarını kullandığınızı kontrol edin
- Aktarım sırasında veri bozulması olup olmadığını kontrol edin
- RSA anahtar çiftinin uyumlu olduğunu doğrulayın
