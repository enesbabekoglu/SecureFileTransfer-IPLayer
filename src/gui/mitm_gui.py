import tkinter as tk
from tkinter import messagebox
import threading
import datetime
from ..utils.mitm_utils import arp_poison

# Program bilgileri
APP_NAME = "Güvenli Dosya Transfer Sistemi"
APP_VERSION = "1.0"
CURRENT_YEAR = datetime.datetime.now().year
COPYRIGHT = f"© {CURRENT_YEAR} - Enes Babekoğlu"

def run_mitm_gui():
    class MitmGUI:
        def __init__(self, root):
            self.root = root
            self.root.title(f"{APP_NAME} - MITM Simülasyonu")
            self.root.geometry("600x400")
            
            # Ana başlık
            tk.Label(root, text=f"{APP_NAME}", font=("Helvetica", 16, "bold")).pack(pady=10)
            tk.Label(root, text="MITM Saldırısı Simülasyonu", font=("Helvetica", 14)).pack(pady=5)
            
            # Ana menüye dönüş butonu
            self.back_button = tk.Button(root, text="Ana Menüye Dön", font=("Helvetica", 10, "bold"), 
                                         bg="#E0E0E0", command=self.return_to_main_menu)
            self.back_button.pack(pady=5)
            
            # Copyright bilgisi ekle
            copyright_label = tk.Label(root, text=COPYRIGHT, font=("Helvetica", 9), fg="gray")
            copyright_label.pack(side=tk.BOTTOM, pady=5)

            frame = tk.Frame(root)
            frame.pack(pady=10)

            tk.Label(frame, text="Hedef IP:").grid(row=0, column=0, sticky="e")
            self.victim_entry = tk.Entry(frame)
            self.victim_entry.grid(row=0, column=1, padx=5)

            tk.Label(frame, text="Gateway IP:").grid(row=1, column=0, sticky="e")
            self.gateway_entry = tk.Entry(frame)
            self.gateway_entry.grid(row=1, column=1, padx=5)

            tk.Label(frame, text="Interface:").grid(row=2, column=0, sticky="e")
            self.iface_entry = tk.Entry(frame)
            self.iface_entry.grid(row=2, column=1, padx=5)

            self.start_btn = tk.Button(root, text="Saldırıyı Başlat", command=self.start, fg="black")
            self.start_btn.pack(pady=5)

            self.log = tk.Text(root, height=10, state=tk.DISABLED)
            self.log.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        def log_message(self, msg):
            self.log.config(state=tk.NORMAL)
            self.log.insert(tk.END, msg + "\n")
            self.log.config(state=tk.DISABLED)
            self.log.see(tk.END)
            
        def return_to_main_menu(self):
            """Ana menüye geri dön"""
            self.root.destroy()
            from src.gui.app import main
            main()

        def start(self):
            victim = self.victim_entry.get().strip()
            gateway = self.gateway_entry.get().strip()
            iface = self.iface_entry.get().strip()
            if not (victim and gateway and iface):
                messagebox.showwarning("Uyarı", "Tüm alanları doldurun.")
                return
            self.start_btn.config(state=tk.DISABLED)
            threading.Thread(
                target=arp_poison,
                args=(victim, gateway, iface, 100, 1, self.log_message),
                daemon=True
            ).start()

    root = tk.Tk()
    MitmGUI(root)
    root.mainloop()
