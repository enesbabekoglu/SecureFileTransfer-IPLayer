import tkinter as tk
from tkinter import messagebox
import socket, os
import struct
import hashlib
import threading
import datetime

# Program bilgileri
APP_NAME = "Güvenli Dosya Transfer Sistemi"
APP_VERSION = "1.0"
CURRENT_YEAR = datetime.datetime.now().year
COPYRIGHT = f"© {CURRENT_YEAR} - Enes Babekoğlu"

from .widgets.file_selector import FileSelector
from ..utils import config
from ..utils.cryptography_utils import generate_aes_key_iv, encrypt_with_aes, encrypt_key_with_rsa
from ..utils.file_utils import read_file_bytes, calculate_sha256
from ..utils.file_chunking_utils import split_file_into_chunks, create_chunk_header, DEFAULT_CHUNK_SIZE, chunk_file_generator

def run_client_gui():
    class ClientGUI:
        def __init__(self, root):
            self.root = root
            self.root.title(f"{APP_NAME} - İstemci Modu")
            self.root.geometry("700x500")
            
            # Thread ve socket durumu için bayrak
            self.running = True
            self.client_socket = None
            self.transfer_thread = None
            
            # Ana başlık
            tk.Label(root, text=f"{APP_NAME}", font=("Helvetica", 16, "bold")).pack(pady=10)
            tk.Label(root, text="İstemci Modu - Dosya Gönderimi", font=("Helvetica", 14)).pack(pady=5)
            
            # Ana menüye dönüş butonu
            self.back_button = tk.Button(root, text="Ana Menüye Dön", font=("Helvetica", 10, "bold"), 
                                         bg="#E0E0E0", command=self.return_to_main_menu)
            self.back_button.pack(pady=5)
            
            # Copyright bilgisi ekle
            copyright_label = tk.Label(root, text=COPYRIGHT, font=("Helvetica", 9), fg="gray")
            copyright_label.pack(side=tk.BOTTOM, pady=5)

            # Sunucu IP
            tk.Label(root, text="Sunucu IP:").pack()
            self.ip_entry = tk.Entry(root)
            self.ip_entry.insert(0, "127.0.0.1")
            self.ip_entry.pack()

            # Port
            tk.Label(root, text="Port:").pack()
            self.port_entry = tk.Entry(root)
            self.port_entry.insert(0, "10000")
            self.port_entry.pack()

            # Token
            tk.Label(root, text="Token:").pack()
            self.token_entry = tk.Entry(root)
            self.token_entry.insert(0, "gizli_token_123")
            self.token_entry.pack()

            # Durum
            self.status_label = tk.Label(root,
                text="Bağlantı durumu: ❌ Bağlı değil", fg="red")
            self.status_label.pack(pady=10)

            # Bağlantıyı test et
            tk.Button(root, text="Sunucuya Bağlan",
                      command=self.test_connection).pack(pady=5)

            # Dosya seçici
            self.file_selector = FileSelector(root)
            self.file_selector.pack(pady=10)

            # Dosya gönderme
            self.send_button = tk.Button(root, text="Dosyayı Gönder",
                                         command=self.send_file,
                                         state=tk.DISABLED)
            self.send_button.pack(pady=5)

        def test_connection(self):
            ip = self.ip_entry.get()
            port = int(self.port_entry.get())
            try:
                s = socket.create_connection((ip, port), timeout=3)
                s.close()
                self.status_label.config(
                    text="Bağlantı durumu: ✅ Sunucuya ulaşılabiliyor",
                    fg="green"
                )
                self.send_button.config(state=tk.NORMAL)
            except Exception as e:
                self.status_label.config(
                    text=f"Bağlantı hatası: {e}", fg="red")
                self.send_button.config(state=tk.DISABLED)

        def return_to_main_menu(self):
            """Ana menüye geri dön
            
            Güvenli şekilde tüm bağlantıları ve kaynakları serbest bırakır
            """
            # Thread'i durdurma bayrağını ayarla
            self.running = False
            
            # Açık soketi kapat
            if hasattr(self, 'client_socket') and self.client_socket is not None:
                try:
                    self.client_socket.close()
                    print("[*] İstemci soketi güvenli bir şekilde kapatıldı")
                except Exception as e:
                    print(f"[!] Soket kapanırken hata: {e}")
                    
            # Thread'i bekle (maksimum 1 saniye)
            if self.transfer_thread and self.transfer_thread.is_alive():
                try:
                    self.transfer_thread.join(1.0)
                    print("[*] Transfer thread'i sonlandırıldı")
                except Exception as e:
                    print(f"[!] Thread sonlandırılırken hata: {e}")

            # Pencereyi kapat ve ana menüye dön
            self.root.destroy()
            from src.gui.app import main
            main()
        
        def send_file(self):
            filepath = self.file_selector.selected_file
            if not filepath:
                messagebox.showwarning("Uyarı", "Lütfen bir dosya seçin.")
                return

            # Ayarları güncelle
            config.SERVER_IP = self.ip_entry.get()
            config.SERVER_PORT = int(self.port_entry.get())
            config.AUTH_TOKEN = self.token_entry.get().encode()
            
            # Arayüz elemanlarını devre dışı bırak
            self.send_button.config(state=tk.DISABLED)
            
            # Thread ile dosya gönderme işlemini başlat
            self.transfer_thread = threading.Thread(target=self._send_file_thread, args=(filepath,), daemon=True)
            self.transfer_thread.start()
            
        def _send_file_thread(self, filepath):
            """Dosya gönderme işlemini arka planda thread olarak gerçekleştir"""
            try:
                # 1. AES key & IV oluştur (tüm parçalar için aynı anahtar kullanacağız)
                aes_key, iv = generate_aes_key_iv()
                
                # 2. AES key + IV'yi birleştirip RSA ile şifrele
                encrypted_key = encrypt_key_with_rsa(config.PUBLIC_KEY_PATH, aes_key + iv)
                
                # 3. Dosya boyutunu al ve toplam parça sayısını hesapla
                chunk_size = DEFAULT_CHUNK_SIZE 
                filesize = os.path.getsize(filepath)
                total_chunks = (filesize + chunk_size - 1) // chunk_size  # Yukarı yuvarlama
                name = os.path.basename(filepath).encode()
                
                # GUI güncellemelerini thread-safe bir şekilde yap
                self.root.after(0, lambda: self.status_label.config(
                    text=f"Dosya gönderiliyor: {name.decode()}, {total_chunks} parça", fg="blue"))
                
                # 4. Socket ile sunucuya bağlan
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.settimeout(10)  # 10 saniye timeout ayarla
                self.client_socket.connect((config.SERVER_IP, config.SERVER_PORT))
                
                # 5. Token gönder
                self.client_socket.sendall(config.AUTH_TOKEN + b"\n")
                
                # 6. Dosya adını ve toplam parça sayısını gönder
                file_info = struct.pack("!I", len(name)) + name + struct.pack("!I", total_chunks)
                self.client_socket.sendall(file_info)
                
                # 7. Şifrelenmiş anahtarı gönder
                key_len_bytes = struct.pack("!I", len(encrypted_key))
                self.client_socket.sendall(key_len_bytes + encrypted_key)
                
                # 8. Dosyayı parçalar halinde gönder
                for i, (chunk_data, chunk_hash) in enumerate(chunk_file_generator(filepath, chunk_size)):
                    # Thread durdurma kontrolü
                    if not self.running:
                        print("[*] Dosya gönderimi kullanıcı tarafından durduruldu")
                        break
                        
                    # 8.1. Parça başlığı oluştur
                    is_last_chunk = (i == total_chunks - 1)
                    header = create_chunk_header(
                        chunk_index=i,
                        total_chunks=total_chunks,
                        chunk_size=len(chunk_data),
                        is_last_chunk=is_last_chunk
                    )
                    
                    # 8.2. Parçayı şifrele
                    encrypted_chunk = encrypt_with_aes(chunk_data, aes_key, iv)
                    
                    # 8.3. Parça hash'ini ekle - ŞİFRELENMEMİŞ veriyi kullanarak hash hesaplıyoruz
                    hash_obj = hashlib.sha256(chunk_data)
                    calculated_hash = hash_obj.hexdigest().encode()
                    print(f"[*] İstemci: Gönderilen parça hash'i: {calculated_hash[:20]}... (uzunluk: {len(calculated_hash)})")
                    chunk_data_with_hash = encrypted_chunk + b'||' + calculated_hash
                    
                    # 8.4. Parça uzunluğunu ve içeriğini gönder
                    data_len_bytes = struct.pack("!I", len(header) + len(chunk_data_with_hash))
                    self.client_socket.sendall(data_len_bytes + header + chunk_data_with_hash)
                    
                    # Durum bilgisini thread-safe bir şekilde güncelle
                    self.root.after(0, lambda c=i, t=total_chunks: self.status_label.config(
                        text=f"Parça {c+1}/{t} gönderildi", fg="blue"))
                
                # İşlem tamam, socket kapatma işlemini güvenli bir şekilde yap
                self.client_socket.close()
                self.client_socket = None
                
                # GUI güncellemelerini thread-safe bir şekilde yap
                self.root.after(0, lambda n=name.decode(): [
                    self.status_label.config(text=f"Dosya başarıyla gönderildi: {n}", fg="green"),
                    messagebox.showinfo("Başarılı", "Dosya başarıyla gönderildi."),
                    self.send_button.config(state=tk.NORMAL)
                ])
                
            except Exception as e:
                # Bağlantı kapalı mı diye kontrol et
                if self.running:  # Sadece kullanıcı kapatmadıysa hata mesajı göster
                    error_msg = str(e)
                    # GUI güncellemelerini thread-safe bir şekilde yap
                    self.root.after(0, lambda msg=error_msg: [
                        self.status_label.config(text=f"Hata: {msg}", fg="red"),
                        messagebox.showerror("Hata", msg),
                        self.send_button.config(state=tk.NORMAL)
                    ])
                
                # Socket kapatma işlemi
                try:
                    if self.client_socket:
                        self.client_socket.close()
                        self.client_socket = None
                except:
                    pass

    root = tk.Tk()
    ClientGUI(root)
    root.mainloop()
