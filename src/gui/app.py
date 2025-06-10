import tkinter as tk
import datetime
from .client_gui import run_client_gui
from .server_gui import run_server_gui
from .mitm_gui import run_mitm_gui
from .network_analysis_gui import NetworkAnalysisGUI

# Program bilgileri
APP_NAME = "Güvenli Dosya Transfer Sistemi"
APP_VERSION = "1.0"
CURRENT_YEAR = datetime.datetime.now().year
COPYRIGHT = f"© {CURRENT_YEAR} - Enes Babekoğlu"

def run_network_analysis_gui():
    app = NetworkAnalysisGUI()
    app.run()

def main():
    root = tk.Tk()
    root.title(f"{APP_NAME} v{APP_VERSION}")
    root.geometry("400x420")

    # Ana başlık
    tk.Label(root, text=APP_NAME, font=("Helvetica", 16, "bold")).pack(pady=10)
    tk.Label(root, text="Mod Seçin", font=("Helvetica", 14)).pack(pady=5)

    # Daha güzel butonlar oluşturalim
    button_style = {"width": 25, "height": 2, "bg": "#E0E0E0", "fg": "black", 
                   "font": ("Helvetica", 12), "relief": tk.RAISED, "borderwidth": 2}
    
    tk.Button(root, text="Sunucu Modu", **button_style,
              command=lambda: (root.destroy(), run_server_gui())
    ).pack(pady=10)

    tk.Button(root, text="İstemci Modu", **button_style,
              command=lambda: (root.destroy(), run_client_gui())
    ).pack(pady=10)

    tk.Button(root, text="Ağ Analizi", **button_style,
              command=lambda: (root.destroy(), run_network_analysis_gui())
    ).pack(pady=10)

    tk.Button(root, text="MITM Saldırısı", **button_style,
              command=lambda: (root.destroy(), run_mitm_gui())
    ).pack(pady=10)

    # Copyright bilgisi ekle
    copyright_label = tk.Label(root, text=COPYRIGHT, font=("Helvetica", 9), fg="gray")
    copyright_label.pack(side=tk.BOTTOM, pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()
