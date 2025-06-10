#!/bin/bash

# Renkli çıktı için kod tanımları
KIRMIZI='\033[0;31m'
YESIL='\033[0;32m'
MAVI='\033[0;34m'
NORMAL='\033[0m'

# Çalışma dizinini script'in bulunduğu dizin olarak ayarla
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo -e "${MAVI}=======================================${NORMAL}"
echo -e "${YESIL}Güvenli Dosya Transfer Sistemi${NORMAL}"
echo -e "${MAVI}=======================================${NORMAL}"

# Sanal ortam kontrol et ve gerekirse oluştur
if [ ! -d "venv" ]; then
    echo -e "${MAVI}[*] Sanal ortam oluşturuluyor...${NORMAL}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${KIRMIZI}[!] Hata: Python3 yüklü değil veya venv oluşturulamadı.${NORMAL}"
        exit 1
    fi
    echo -e "${YESIL}[+] Sanal ortam oluşturuldu.${NORMAL}"
else
    echo -e "${YESIL}[+] Mevcut sanal ortam kullanılıyor.${NORMAL}"
fi

# Sanal ortamı aktifleştir
echo -e "${MAVI}[*] Sanal ortam aktifleştiriliyor...${NORMAL}"
source venv/bin/activate

# Gereklilikleri kur
echo -e "${MAVI}[*] Gerekli kütüphaneler yükleniyor...${NORMAL}"
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${KIRMIZI}[!] Kütüphaneler yüklenemedi.${NORMAL}"
    deactivate
    exit 1
fi

echo -e "${YESIL}[+] Kütüphaneler yüklendi.${NORMAL}"

echo -e "${MAVI}[*] Uygulama başlatılıyor...${NORMAL}"
echo ""

# Uygulamayı çalıştır
python -m src.server.server &
sleep 2
python -m src.gui.app

# Sanal ortamı deaktive et
deactivate
pkill -f "python -m src.server.server"

echo -e "${YESIL}[+] Program sonlandı.
Çıkmak için Enter'a basın.${NORMAL}"
read
