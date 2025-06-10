@echo off
color 0A

echo ======================================================
echo Guvenli Dosya Transfer Sistemi Baslatiliyor...
echo ======================================================

:: Calisma dizinini script'in bulundugu dizin olarak ayarla
cd /d "%~dp0"

:: Sanal ortam kontrol et ve gerekirse olustur
if not exist venv (
    echo Sanal ortam bulunamadi, olusturuluyor...
    python -m venv venv
    if errorlevel 1 (
        echo Sanal ortam olusturma hatasi! Python yuklu oldugundan emin olun.
        pause
        exit /b 1
    )
    echo Sanal ortam basariyla olusturuldu.
) else (
    echo Sanal ortam zaten var, kullanilacak.
)

:: Sanal ortami aktifleştir
echo Sanal ortam aktiflestiriliyor...
call venv\Scripts\activate.bat

:: Gereklilikleri kur
echo Gereksinimler kontrol ediliyor ve kuruluyor...
pip install -r requirements.txt

if errorlevel 1 (
    echo Gereksinimlerin kurulumunda hata! Tekrar deneyin.
    call venv\Scripts\deactivate.bat
    pause
    exit /b 1
)

echo Tum gereksinimler kuruldu.

:: Programi baslat
echo ======================================================
echo Program baslatiliyor...
echo ======================================================

:: GUI uygulamasini baslat
python -m src.gui.app

:: Sanal ortami devre dışı birak
call venv\Scripts\deactivate.bat

echo ======================================================
echo Program sonlandi.
echo ======================================================
pause
