#!/bin/bash

# Çalışma dizinini script'in bulunduğu dizin olarak ayarla
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Uygulamanın adını ekranda göster
echo "=================================================="
echo "    Güvenli Dosya Transfer Sistemi Başlatılıyor   "
echo "=================================================="

# Sanal ortam kontrol et ve gerekirse oluştur
if [ ! -d "venv" ]; then
    echo "[*] Sanal ortam oluşturuluyor..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[!] Hata: Python3 yüklü değil veya venv oluşturulamadı."
        echo "Çıkmak için bir tuşa basın."
        read -n 1 -s
        exit 1
    fi
    echo "[+] Sanal ortam oluşturuldu."
else
    echo "[+] Mevcut sanal ortam kullanılıyor."
fi

# Sanal ortamı aktifleştir
echo "[*] Sanal ortam aktifleştiriliyor..."
source venv/bin/activate

# Gereklilikleri kur
echo "[*] Gerekli kütüphaneler kontrol ediliyor..."
pip install -r requirements.txt > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "[!] Kütüphaneler yüklenemedi."
    deactivate
    echo "Çıkmak için bir tuşa basın."
    read -n 1 -s
    exit 1
fi

echo "[+] Kütüphaneler hazır."
echo "[*] Uygulama başlatılıyor..."

# Sunucuyu arka planda çalıştır
python -m src.server.server &
SERVER_PID=$!
sleep 2

# GUI uygulamasını başlat
python -m src.gui.app

# Sunucuyu kapat
kill $SERVER_PID 2>/dev/null

# Sanal ortamı deaktive et
deactivate

echo "[+] Program sonlandı."
echo "Çıkmak için Enter'a basın."
read
