import tkinter as tk
import threading
import socket
import sys
import datetime

# Program bilgileri
APP_NAME = "Güvenli Dosya Transfer Sistemi"
APP_VERSION = "1.0"
CURRENT_YEAR = datetime.datetime.now().year
COPYRIGHT = f"© {CURRENT_YEAR} - Enes Babekoğlu"

from ..utils import config
from ..server.network_server import handle_incoming_connection

def run_server_gui():
    class ServerGUI:
        def __init__(self, root):
            self.root = root
            self.root.title(f"{APP_NAME} - Sunucu Modu")
            self.root.geometry("600x400")
            
            # Thread kontrolü için flag
            self.running = False
            self.server_thread = None
            self.server_socket = None
            
            # Ana başlık
            tk.Label(root, text=f"{APP_NAME}", font=("Helvetica", 16, "bold")).pack(pady=10)
            tk.Label(root, text="Sunucu Modu - Dinleyici", font=("Helvetica", 14)).pack(pady=5)
            
            # Ana menüye dönüş butonu
            self.back_button = tk.Button(root, text="Ana Menüye Dön", font=("Helvetica", 10, "bold"), 
                                         bg="#E0E0E0", command=self.return_to_main_menu)
            self.back_button.pack(pady=5)
            
            # Copyright bilgisi ekle
            copyright_label = tk.Label(root, text=COPYRIGHT, font=("Helvetica", 9), fg="gray")
            copyright_label.pack(side=tk.BOTTOM, pady=5)

            self.status_label = tk.Label(root,
                text="Sunucu durumu: 🔴 Kapalı", fg="red")
            self.status_label.pack(pady=10)

            self.start_button = tk.Button(root, text="Sunucuyu Başlat",
                                          command=self.start_server)
            self.start_button.pack(pady=5)

            self.log = tk.Text(root, height=10, state=tk.DISABLED)
            self.log.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        def log_message(self, msg):
            self.log.config(state=tk.NORMAL)
            self.log.insert(tk.END, msg + "\n")
            self.log.config(state=tk.DISABLED)
            self.log.see(tk.END)
            
        def return_to_main_menu(self):
            """Ana menüye geri dön"""
            # Server thread'i durdur
            self.running = False
            
            # Eğer socket açıksa kapat
            if self.server_socket:
                try:
                    self.server_socket.close()
                except:
                    pass
                    
            # Pencereyi kapat ve ana menüye dön
            self.root.destroy()
            from src.gui.app import main
            main()

        def start_server(self):
            self.status_label.config(
                text="Sunucu durumu: 🟢 Dinleniyor", fg="green")
            self.start_button.config(state=tk.DISABLED)
            
            # Thread durumunu çalışıyor olarak ayarla
            self.running = True
            
            # Yeni thread oluştur ve başlat
            self.server_thread = threading.Thread(target=self.server_loop, daemon=True)
            self.server_thread.start()

        def server_loop(self):
            try:
                # Socket oluştur
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
                # Portu tekrar kullanabilmek için SO_REUSEADDR ayarı
                self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                
                # 5 saniye timeout ayarla, böylece döngü kontrolü mümkün olur
                self.server_socket.settimeout(5)
                
                self.server_socket.bind(("0.0.0.0", config.SERVER_PORT))
                self.server_socket.listen(1)
                self.log_message(f"[+] Port {config.SERVER_PORT} dinleniyor...")
                
                # Thread çalıştığı sürece devam et
                while self.running:
                    try:
                        conn, addr = self.server_socket.accept()
                        if self.running:  # Eğer hala çalışıyorsa
                            try:
                                self.log_message(f"[+] Bağlantı geldi: {addr}")
                                threading.Thread(
                                    target=handle_incoming_connection,
                                    args=(conn, addr, self.log_message),
                                    daemon=True
                                ).start()
                            except Exception as e:
                                print(f"Bağlantı işleme hatası: {e}")
                    except socket.timeout:
                        # Timeout döngü kontrolü için kullanılıyor
                        continue
                    except Exception as e:
                        if self.running:  # Sadece çalışıyorsa hata mesajı göster
                            print(f"Sunucu döngüsünde hata: {e}")
                        break
            except Exception as e:
                print(f"Sunucu başlatma hatası: {e}")
            finally:
                # Socket'i kapatmaya çalış
                if self.server_socket:
                    try:
                        self.server_socket.close()
                    except:
                        pass

    root = tk.Tk()
    ServerGUI(root)
    root.mainloop()
