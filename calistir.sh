#!/bin/bash

# Renkli çıktı için kod tanımları
KIRMIZI='\033[0;31m'
YESIL='\033[0;32m'
MAVI='\033[0;34m'
NORMAL='\033[0m'

# Sanal ortamı aktifleştir
source venv/bin/activate

# Programı çalıştır
echo -e "${MAVI}===========================================${NORMAL}"
echo -e "${YESIL}Güvenli Dosya Transfer Sistemi Başlatıldı${NORMAL}"
echo -e "${MAVI}===========================================${NORMAL}"
echo ""

# Programı çalıştır
python -m src.gui.app

# Sanal ortamı deaktive et
deactivate

echo ""
echo -e "${MAVI}===========================================${NORMAL}"
echo -e "${YESIL}Program sonlandı. Çıkmak için Enter'a basın${NORMAL}"
echo -e "${MAVI}===========================================${NORMAL}"
read
