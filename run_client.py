#!/usr/bin/env python3
"""
Basit istemci başlatma
"""
import sys
import os
import time

# Ana dizini ekleyerek modüllere erişelim
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

# İstemci modülünü import et
from src.gui.client_gui import run_client_gui

if __name__ == "__main__":
    print("İstemci başlatılıyor...")
    run_client_gui()
