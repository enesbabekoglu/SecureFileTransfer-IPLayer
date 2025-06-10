#!/usr/bin/env python3
"""
Basit sunucu başlatma
"""
import sys
import os
import time

# Ana dizini ekleyerek modüllere erişelim
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

# Sunucu modülünü import et
from src.gui.server_gui import run_server_gui

if __name__ == "__main__":
    print("Sunucu başlatılıyor...")
    run_server_gui()
