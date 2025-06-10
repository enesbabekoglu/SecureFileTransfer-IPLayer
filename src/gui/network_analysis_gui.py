#!/usr/bin/env python3
"""
Ağ Analiz GUI Modülü - IP başlık işleme ve ağ performans ölçümü için kullanıcı arayüzü
"""
import os
import sys
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import json
import time
import platform

# Matplotlib için gerekli importlar (grafikler için)
try:
    # Matplotlib backend'i önce ayarlayalım (GUI başlamadan önce yapılmalı)
    import matplotlib
    # Backend ayarını yap (MacOS ve Linux için)
    if platform.system() == "Darwin":  # MacOS
        matplotlib.use("TkAgg")
    elif platform.system() == "Linux":
        matplotlib.use("TkAgg")
    # Gerekli modülleri import et
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import numpy as np  # Matplotlib ile birlikte genelde numpy kullanılır
    MATPLOTLIB_AVAILABLE = True
    print("Matplotlib başarıyla yüklendi.")
except Exception as e:
    MATPLOTLIB_AVAILABLE = False
    print(f"Uyarı: Matplotlib yüklenemedi. Hata: {str(e)}. Grafikler devre dışı.")
    # Matplotlib olmadan da çalışabilmek için boş sınıflar oluşturalım
    class Figure:
        def __init__(self, *args, **kwargs):
            pass
        
        def add_subplot(self, *args, **kwargs):
            return type('obj', (object,), {'plot': lambda *args, **kwargs: None})
    
    class FigureCanvasTkAgg:
        def __init__(self, *args, **kwargs):
            pass
        
        def get_tk_widget(self):
            return tk.Frame()  # Boş bir frame döndür
        
        def draw(self):
            pass

# Kendi modüllerimizi import et
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.ip_header_utils import create_custom_ip_packet, calculate_ip_checksum, validate_ip_checksum, analyze_ip_header
from utils.network_performance_utils import measure_rtt_ping, measure_bandwidth_socket, simulate_network_conditions, compare_network_conditions

class NetworkAnalysisGUI:
    """Ağ Analizi için Grafik Kullanıcı Arayüzü"""
    
    def __init__(self, root=None):
        """NetworkAnalysisGUI sınıfının başlatıcısı"""
        if root is None:
            self.root = tk.Tk()
            self.root.title("Ağ Analiz Aracı")
            self.root.geometry("800x600")
        else:
            self.root = root
            
        # Thread kontrol bayrakları
        self.running = True
        self.bandwidth_thread = None
        self.ping_thread = None
        self.test_thread = None
        self.network_condition_thread = None
            
        # Ana menüye dönüş butonu
        self.back_button = tk.Button(self.root, text="Ana Menüye Dön", command=self.return_to_main_menu)
        self.back_button.pack(pady=5)
            
        # Ana sekme penceresi oluştur
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sekmeleri oluştur
        self.create_ip_header_tab()
        self.create_ping_tab()
        self.create_bandwidth_tab()
        self.create_network_conditions_tab()
    
    def create_ip_header_tab(self):
        """IP başlık işleme için sekme oluşturur"""
        self.ip_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.ip_frame, text="IP Başlık İşleme")
        
        # Hedef IP kısmı
        ttk.Label(self.ip_frame, text="Hedef IP:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.dst_ip_entry = ttk.Entry(self.ip_frame, width=20)
        self.dst_ip_entry.grid(row=0, column=1, padx=5, pady=5)
        self.dst_ip_entry.insert(0, "8.8.8.8")  # Varsayılan olarak Google DNS
        
        # Kaynak IP kısmı (opsiyonel)
        ttk.Label(self.ip_frame, text="Kaynak IP (opsiyonel):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.src_ip_entry = ttk.Entry(self.ip_frame, width=20)
        self.src_ip_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # TTL kısmı
        ttk.Label(self.ip_frame, text="TTL:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.ttl_spinbox = ttk.Spinbox(self.ip_frame, from_=1, to=255, width=10)
        self.ttl_spinbox.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.ttl_spinbox.insert(0, "64")  # Varsayılan TTL değeri
        
        # IP Bayrakları kısmı
        ttk.Label(self.ip_frame, text="IP Bayrakları:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.flag_frame = ttk.Frame(self.ip_frame)
        self.flag_frame.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        
        self.df_var = tk.IntVar()
        self.df_var.set(1)  # Varsayılan olarak DF (Don't Fragment) aktif
        self.df_check = ttk.Checkbutton(self.flag_frame, text="DF (Don't Fragment)", variable=self.df_var)
        self.df_check.grid(row=0, column=0)
        
        self.mf_var = tk.IntVar()
        self.mf_check = ttk.Checkbutton(self.flag_frame, text="MF (More Fragments)", variable=self.mf_var)
        self.mf_check.grid(row=0, column=1)
        
        # Fragment Offset kısmı
        ttk.Label(self.ip_frame, text="Fragment Offset:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.frag_spinbox = ttk.Spinbox(self.ip_frame, from_=0, to=8191, width=10)
        self.frag_spinbox.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        self.frag_spinbox.insert(0, "0")  # Varsayılan fragment offset değeri
        
        # Ayırıcı
        ttk.Separator(self.ip_frame, orient="horizontal").grid(row=5, column=0, columnspan=2, sticky="ew", padx=5, pady=10)
        
        # Butonlar
        button_frame = ttk.Frame(self.ip_frame)
        button_frame.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        
        self.create_packet_btn = ttk.Button(button_frame, text="Paket Oluştur", command=self.create_packet)
        self.create_packet_btn.grid(row=0, column=0, padx=5, pady=5)
        
        self.calc_checksum_btn = ttk.Button(button_frame, text="Checksum Hesapla", command=self.calculate_packet_checksum)
        self.calc_checksum_btn.grid(row=0, column=1, padx=5, pady=5)
        
        self.fragment_btn = ttk.Button(button_frame, text="Paketi Parçala ve Gönder", command=self.fragment_packet)
        self.fragment_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Sonuç alanı
        ttk.Label(self.ip_frame, text="Paket Bilgileri:").grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
        self.packet_info_text = scrolledtext.ScrolledText(self.ip_frame, width=60, height=15)
        self.packet_info_text.grid(row=8, column=0, columnspan=2, padx=5, pady=5)
        
        # Paket değişkenimiz
        self.current_packet = None
    
    def create_ping_tab(self):
        """Ping testi için sekme oluşturur"""
        self.ping_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.ping_frame, text="Ping Testi")
        
        # Hedef ayarları
        ttk.Label(self.ping_frame, text="Hedef IP:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.ping_target_entry = ttk.Entry(self.ping_frame, width=30)
        self.ping_target_entry.grid(row=0, column=1, padx=5, pady=5)
        self.ping_target_entry.insert(0, "8.8.8.8")  # varsayılan değer
        
        # Ping sayısı
        ttk.Label(self.ping_frame, text="Ping Sayısı:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.ping_count_spinbox = ttk.Spinbox(self.ping_frame, from_=1, to=100, width=10)
        self.ping_count_spinbox.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.ping_count_spinbox.insert(0, "5")  # varsayılan değer
        
        # Ping butonları
        button_frame = ttk.Frame(self.ping_frame)
        button_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        
        self.start_ping_btn = ttk.Button(button_frame, text="Ping Testi Başlat", command=self.start_ping_test)
        self.start_ping_btn.grid(row=0, column=0, padx=5, pady=5)
        
        # Sonuç metin alanı
        self.ping_result_text = scrolledtext.ScrolledText(self.ping_frame, width=60, height=15)
        self.ping_result_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        
        # Grafik alanı
        if MATPLOTLIB_AVAILABLE:
            self.ping_fig = Figure(figsize=(7, 3))
            self.ping_ax = self.ping_fig.add_subplot(111)
            self.ping_ax.set_title("RTT Ölçüm Sonuçları")
            self.ping_ax.set_xlabel("Ping Sırası")
            self.ping_ax.set_ylabel("RTT (ms)")
            
            self.ping_canvas = FigureCanvasTkAgg(self.ping_fig, master=self.ping_frame)
            self.ping_canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, padx=5, pady=5)
            
            # Grafik için veri depolama listesi
            self.ping_data = []
        else:
            ttk.Label(self.ping_frame, text="Grafik görüntülemek için matplotlib gereklidir.", 
                     foreground="red").grid(row=4, column=0, columnspan=2, padx=5, pady=5)
    
    def create_bandwidth_tab(self):
        """Bant genişliği testi için sekme oluşturur"""
        self.bandwidth_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.bandwidth_frame, text="Bant Genişliği")
        
        # Hedef ayarları
        ttk.Label(self.bandwidth_frame, text="Hedef Sunucu:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.bw_server_entry = ttk.Entry(self.bandwidth_frame, width=30)
        self.bw_server_entry.grid(row=0, column=1, padx=5, pady=5)
        self.bw_server_entry.insert(0, "localhost")  # varsayılan değer
        
        # Port numarası
        ttk.Label(self.bandwidth_frame, text="Port Numarası:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.bw_port_entry = ttk.Entry(self.bandwidth_frame, width=10)
        self.bw_port_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.bw_port_entry.insert(0, "5201")  # iPerf3 için varsayılan port
        
        # Test süresi
        ttk.Label(self.bandwidth_frame, text="Test Süresi (saniye):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.bw_duration_spinbox = ttk.Spinbox(self.bandwidth_frame, from_=1, to=60, width=10)
        self.bw_duration_spinbox.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.bw_duration_spinbox.insert(0, "5")  # varsayılan değer
        
        # Test modu seçenekleri
        ttk.Label(self.bandwidth_frame, text="Test Modu:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.bw_mode_frame = ttk.Frame(self.bandwidth_frame)
        self.bw_mode_frame.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        
        self.bw_mode_var = tk.StringVar(value="client")
        self.bw_client_radio = ttk.Radiobutton(self.bw_mode_frame, text="Client", variable=self.bw_mode_var, value="client")
        self.bw_client_radio.grid(row=0, column=0, padx=5)
        
        self.bw_server_radio = ttk.Radiobutton(self.bw_mode_frame, text="Server", variable=self.bw_mode_var, value="server")
        self.bw_server_radio.grid(row=0, column=1, padx=5)
        
        # Test butonları
        button_frame = ttk.Frame(self.bandwidth_frame)
        button_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=10)
        
        self.start_bw_test_btn = ttk.Button(button_frame, text="Bant Genişliği Testi Başlat", command=self.start_bandwidth_test)
        self.start_bw_test_btn.grid(row=0, column=0, padx=5, pady=5)
        
        self.install_iperf_btn = ttk.Button(button_frame, text="iPerf3 Kur", command=self.install_iperf)
        self.install_iperf_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # Sonuç metin alanı
        self.bw_result_text = scrolledtext.ScrolledText(self.bandwidth_frame, width=60, height=15)
        self.bw_result_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        
        # Grafik alanı (gelecekte eklenebilir)
    
    def create_network_conditions_tab(self):
        """Ağ koşulları simülasyonu için sekme oluşturur"""
        self.network_conditions_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.network_conditions_frame, text="Ağ Koşulları")
        
        # Ağ arayüzü seçimi
        ttk.Label(self.network_conditions_frame, text="Ağ Arayüzü:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.interface_entry = ttk.Entry(self.network_conditions_frame, width=30)
        self.interface_entry.grid(row=0, column=1, padx=5, pady=5, columnspan=2)
        self.interface_entry.insert(0, "eth0")  # Linux için varsayılan
        
        # Kullanılabilir ağ arayüzlerini listele butonu
        self.list_interfaces_btn = ttk.Button(self.network_conditions_frame, text="Ağ Arayüzlerini Listele", 
                                            command=self.list_network_interfaces)
        self.list_interfaces_btn.grid(row=0, column=3, padx=5, pady=5)
        
        # Gecikme ayarı
        ttk.Label(self.network_conditions_frame, text="Gecikme (ms):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.delay_spinbox = ttk.Spinbox(self.network_conditions_frame, from_=0, to=1000, width=10)
        self.delay_spinbox.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.delay_spinbox.insert(0, "100")  # varsayılan değer
        
        # Gecikme değişkenliği
        ttk.Label(self.network_conditions_frame, text="Gecikme Değişkenliği (ms):").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.jitter_spinbox = ttk.Spinbox(self.network_conditions_frame, from_=0, to=100, width=10)
        self.jitter_spinbox.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)
        self.jitter_spinbox.insert(0, "10")  # varsayılan değer
        
        # Paket kaybı
        ttk.Label(self.network_conditions_frame, text="Paket Kaybı (%):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.packet_loss_spinbox = ttk.Spinbox(self.network_conditions_frame, from_=0, to=100, width=10)
        self.packet_loss_spinbox.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.packet_loss_spinbox.insert(0, "1")  # varsayılan değer
        
        # Bant genişliği kısıtlama
        ttk.Label(self.network_conditions_frame, text="Bant Genişliği Limiti (kbps):").grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
        self.bandwidth_spinbox = ttk.Spinbox(self.network_conditions_frame, from_=0, to=100000, width=10)
        self.bandwidth_spinbox.grid(row=2, column=3, padx=5, pady=5, sticky=tk.W)
        self.bandwidth_spinbox.insert(0, "1000")  # varsayılan değer
        
        # Butonlar
        button_frame = ttk.Frame(self.network_conditions_frame)
        button_frame.grid(row=3, column=0, columnspan=4, padx=5, pady=10)
        
        self.apply_conditions_btn = ttk.Button(button_frame, text="Koşulları Uygula", 
                                              command=self.apply_network_conditions)
        self.apply_conditions_btn.grid(row=0, column=0, padx=5, pady=5)
        
        self.reset_conditions_btn = ttk.Button(button_frame, text="Koşulları Sıfırla", 
                                             command=self.reset_network_conditions)
        self.reset_conditions_btn.grid(row=0, column=1, padx=5, pady=5)
        
        self.test_conditions_btn = ttk.Button(button_frame, text="Koşulları Test Et", 
                                            command=self.test_network_conditions)
        self.test_conditions_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Sonuç metin alanı
        self.net_cond_result_text = scrolledtext.ScrolledText(self.network_conditions_frame, width=60, height=15)
        self.net_cond_result_text.grid(row=4, column=0, columnspan=4, padx=5, pady=5)
        
        # Platform uyumlukluk uyarısı ekle
        platform_frame = ttk.Frame(self.network_conditions_frame)
        platform_frame.grid(row=5, column=0, columnspan=4, padx=5, pady=5)
        
        import platform
        os_name = platform.system()
        
        if os_name == "Linux":
            platform_msg = "Ağ koşulları simülasyonu Linux'ta 'tc' komutu ile desteklenmektedir."
            msg_color = "black"
        else:
            platform_msg = (f"İşletim sisteminiz ({os_name}) için ağ koşulları simülasyonu sınırlıdır. " 
                           f"Charles Proxy veya Fiddler gibi araçları kullanınız.")
            msg_color = "red"
            
        ttk.Label(platform_frame, text=platform_msg, foreground=msg_color).grid(row=0, column=0, padx=5, pady=5)
    
    def create_packet(self):
        """Kullanıcı tarafından belirlenen özelliklere göre IP paketi oluşturur"""
        try:
            dst_ip = self.dst_ip_entry.get()
            src_ip = self.src_ip_entry.get() if self.src_ip_entry.get() else None
            ttl = int(self.ttl_spinbox.get())
            
            # Bayrakları ayarla
            flags = ""
            if self.df_var.get():
                flags += "DF"
            if self.mf_var.get():
                flags += "+MF"
            
            frag = int(self.frag_spinbox.get())
            
            # Paketi oluştur
            self.current_packet = create_custom_ip_packet(dst_ip, src_ip, ttl, flags, frag)
            
            # Paket bilgilerini göster
            self.display_packet_info()
            
            messagebox.showinfo("Başarılı", "IP paketi başarıyla oluşturuldu.")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Paket oluşturulurken hata: {str(e)}")
    
    def calculate_packet_checksum(self):
        """Oluşturulan paketteki IP checksumını hesaplar ve gösterir"""
        if self.current_packet is None:
            messagebox.showwarning("Uyarı", "Önce bir paket oluşturmalısınız.")
            return
        
        try:
            # Checksum hesapla
            checksum = calculate_ip_checksum(self.current_packet)
            
            # Sonucu göster
            self.packet_info_text.insert(tk.END, f"\n\nHesaplanan IP Checksum: {hex(checksum)}\n")
            messagebox.showinfo("Başarılı", f"IP checksum hesaplandı: {hex(checksum)}")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Checksum hesaplanırken hata: {str(e)}")
    
    def fragment_packet(self):
        """Oluşturulan paketi belirli boyutlara parçalar ve gönderir"""
        if self.current_packet is None:
            messagebox.showwarning("Uyarı", "Önce bir paket oluşturmalısınız.")
            return
        
        # Basit bir iletişim protokolü ekleyelim (örnek olarak ICMP)
        try:
            from scapy.all import ICMP, fragment
            
            # ICMP yükü ekle
            packet_with_payload = self.current_packet / ICMP(type=8, code=0) / (b"A" * 1000)
            
            # Kullanıcıya bilgi ver
            self.packet_info_text.insert(tk.END, "\n\nPaket parçalanıyor ve gönderiliyor...\n")
            
            # Paketin parçalanması için bir thread başlat
            def send_fragments():
                try:
                    # Paketi parçala
                    frags = fragment(packet_with_payload, fragsize=500)
                    
                    # Parçaları göster
                    self.packet_info_text.insert(tk.END, f"\nPaket {len(frags)} parçaya ayrıldı:\n")
                    
                    for i, frag in enumerate(frags):
                        self.packet_info_text.insert(tk.END, f"Parça {i+1}:\n")
                        self.packet_info_text.insert(tk.END, f"  Flags: {frag.flags}\n")
                        self.packet_info_text.insert(tk.END, f"  Frag: {frag.frag}\n")
                        self.packet_info_text.insert(tk.END, f"  Boyut: {len(frag)} bayt\n")
                    
                    # Parçaları gönder
                    # Not: Gerçek gönderme işlemi scapy'nin admin/root yetkisi gerektirir
                    # Bu yüzden sadece parçaları oluşturuyoruz
                    
                    self.packet_info_text.insert(tk.END, "\nParçalar başarıyla oluşturuldu!\n")
                    self.packet_info_text.insert(tk.END, "Not: Gerçek gönderme işlemi için yönetici yetkileri gereklidir.\n")
                    
                except Exception as e:
                    self.packet_info_text.insert(tk.END, f"\nHata: {str(e)}\n")
            
            # Thread başlat
            threading.Thread(target=send_fragments, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Hata", f"Paket parçalanırken hata: {str(e)}")
    
    def display_packet_info(self):
        """Oluşturulan paket bilgilerini gösterir"""
        if self.current_packet is None:
            return
        
        # Tüm paket bilgilerini al
        packet_info = analyze_ip_header(self.current_packet)
        
        # Bilgileri temizle ve ekle
        self.packet_info_text.delete(1.0, tk.END)
        self.packet_info_text.insert(tk.END, "IP Paket Bilgileri:\n")
        self.packet_info_text.insert(tk.END, "=================\n")
        
        for key, value in packet_info.items():
            self.packet_info_text.insert(tk.END, f"{key}: {value}\n")
        
        # Paket özetini göster
        self.packet_info_text.insert(tk.END, "\nPaket Özeti:\n")
        self.packet_info_text.insert(tk.END, str(self.current_packet))
        
    def start_bandwidth_test(self):
        """Bant genişliği testini başlatır"""
        # Değerleri al
        server = self.bw_server_entry.get()
        mode = self.bw_mode_var.get()
        
        try:
            port = int(self.bw_port_entry.get())
            duration = int(self.bw_duration_spinbox.get())
        except ValueError:
            messagebox.showerror("Hata", "Port ve test süresi geçerli sayılar olmalıdır!")
            return
        
        # Eğer server modunda çalışıyorsa rastgele port seç
        if mode == "server":
            import random
            port = random.randint(10000, 20000)  # Rastgele bir port seç
            self.bw_port_entry.delete(0, tk.END)
            self.bw_port_entry.insert(0, str(port))
        
        # Metin alanını temizle
        self.bw_result_text.delete(1.0, tk.END)
        self.bw_result_text.insert(tk.END, f"Bant genişliği testi başlatılıyor ({mode} modu)...\n")
        
        # Test butonunu devre dışı bırak
        self.start_bw_test_btn["state"] = "disabled"
        
        # Testi arka planda çalıştır
        def run_test_thread():
            try:
                # Bu değişkenleri thread içinde kullanmak için
                # baştan tanımlıyoruz
                _server = server
                _port = port
                _mode = mode
                _duration = duration
                
                import subprocess
                import json
                import shutil
                
                # iPerf3'ün kurulu olup olmadığını kontrol et
                iperf3_path = shutil.which("iperf3")
                
                if not iperf3_path:
                    self.bw_result_text.insert(tk.END, "\niPerf3 bulunamadı. Lütfen 'iPerf3 Kur' butonunu kullanarak kurunuz.\n")
                    return
                
                # Komut satırını oluştur
                if _mode == "server":
                    cmd = ["iperf3", "-s", "-p", str(_port), "-1"]  # -1 ile sadece bir test için sunucu çalıştır
                    self.bw_result_text.insert(tk.END, f"Sunucu modu başlatılıyor (port: {_port})...\n")
                    self.bw_result_text.insert(tk.END, "Bir istemci bağlanana kadar bekleniliyor...\n")
                else:  # client mode
                    cmd = ["iperf3", "-c", _server, "-p", str(_port), "-t", str(_duration), "-J"]
                    self.bw_result_text.insert(tk.END, f"{_server}:{_port} adresine istemci olarak bağlanılıyor...\n")
                
                # Komutu çalıştır
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate()
                
                # Sonuçları görüntüle
                if process.returncode == 0:
                    if _mode == "client":
                        try:
                            # JSON sonuçlarını ayrıştır
                            result = json.loads(stdout)
                            
                            # Sonuçları göster (ana thread'de)
                            def update_results():
                                self.bw_result_text.insert(tk.END, "\nTest Sonuçları:\n")
                                self.bw_result_text.insert(tk.END, f"  Sunucu: {result.get('start', {}).get('connected', [])[0].get('remote_host', 'bilinmiyor')}\n")
                                self.bw_result_text.insert(tk.END, f"  Test Süresi: {result.get('end', {}).get('sum_received', {}).get('seconds', 0):.2f} saniye\n")
                                self.bw_result_text.insert(tk.END, f"  Transfer Edilen: {result.get('end', {}).get('sum_received', {}).get('bytes', 0) / 1_000_000:.2f} MB\n")
                                
                                # Bant genişliği değerlerini göster
                                bps = result.get('end', {}).get('sum_received', {}).get('bits_per_second', 0)
                                self.bw_result_text.insert(tk.END, f"  Bant Genişliği: {bps / 1_000_000:.2f} Mbps\n")
                                
                                self.start_bw_test_btn["state"] = "normal"
                            
                            # GUI güncellemesini ana thread'de yap
                            self.root.after(0, update_results)
                            return
                            
                        except json.JSONDecodeError:
                            # Eğer JSON ayrıştırılamazsa ham çıktıyı göster
                            def show_raw():
                                self.bw_result_text.insert(tk.END, "\nHam Sonuçlar:\n")
                                self.bw_result_text.insert(tk.END, stdout)
                                self.start_bw_test_btn["state"] = "normal"
                            
                            self.root.after(0, show_raw)
                            return
                    else:
                        # Sunucu modu sonuçlarını göster
                        def show_server_results():
                            self.bw_result_text.insert(tk.END, "\nSunucu Çalıştırma Sonuçları:\n")
                            self.bw_result_text.insert(tk.END, stdout)
                            self.start_bw_test_btn["state"] = "normal"
                        
                        self.root.after(0, show_server_results)
                        return
                else:
                    # Hata mesajını göster
                    def show_error():
                        self.bw_result_text.insert(tk.END, f"\nHata oluştu (kod: {process.returncode}):\n")
                        self.bw_result_text.insert(tk.END, stderr)
                        self.start_bw_test_btn["state"] = "normal"
                    
                    self.root.after(0, show_error)
                    return
                
            except Exception as e:
                # Hata mesajını göster
                def show_exception():
                    self.bw_result_text.insert(tk.END, f"\nBant genişliği testi sırasında hata: {str(e)}\n")
                    self.start_bw_test_btn["state"] = "normal"
                
                self.root.after(0, show_exception)
        
        # Test thread'ini başlat
        self.bandwidth_thread = threading.Thread(target=run_test_thread, daemon=True)
        self.bandwidth_thread.start()
    
    def install_iperf(self):
        """iPerf3 kurulumunu yönetir"""
        # Metin alanını temizle
        self.bw_result_text.delete(1.0, tk.END)
        self.bw_result_text.insert(tk.END, "iPerf3 kurulumu kontrol ediliyor...\n")
        
    def list_network_interfaces(self):
        """Sistemdeki ağ arayüzlerini listeler"""
        # Sonuç alanını temizle
        self.net_cond_result_text.delete(1.0, tk.END)
        self.net_cond_result_text.insert(tk.END, "Ağ arayüzleri listeleniyor...\n\n")
        
    def apply_network_conditions(self):
        """Seçili ağ koşullarını uygular"""
        interface = self.interface_entry.get()
        
        try:
            delay = int(self.delay_spinbox.get())
            jitter = int(self.jitter_spinbox.get())
            packet_loss = float(self.packet_loss_spinbox.get())
            bandwidth = int(self.bandwidth_spinbox.get())  # kbps cinsinden
        except ValueError:
            messagebox.showerror("Hata", "Tüm parametreler geçerli sayılar olmalıdır!")
            return
        
        # Sonuç alanını temizle
        self.net_cond_result_text.delete(1.0, tk.END)
        self.net_cond_result_text.insert(tk.END, f"{interface} arayüzünde ağ koşulları uygulanıyor...\n\n")
        
        # Bilgi ekle
        self.net_cond_result_text.insert(tk.END, f"Uygulanacak koşullar:\n")
        self.net_cond_result_text.insert(tk.END, f"  Gecikme: {delay} ms\n")
        self.net_cond_result_text.insert(tk.END, f"  Gecikme Değişkenliği: {jitter} ms\n")
        self.net_cond_result_text.insert(tk.END, f"  Paket Kaybı: {packet_loss}%\n")
        self.net_cond_result_text.insert(tk.END, f"  Bant Genişliği Limiti: {bandwidth} kbps\n\n")
        
        def run_apply_conditions():
            try:
                import platform
                import subprocess
                import os
                
                os_name = platform.system()
                
                if os_name != "Linux":
                    self.net_cond_result_text.insert(tk.END, "Bu özellik yalnızca Linux'ta desteklenmektedir.\n")
                    self.net_cond_result_text.insert(tk.END, "Diğer işletim sistemleri için Charles Proxy veya Fiddler kullanabilirsiniz.\n")
                    return
                
                # Root yetkisi kontrol et
                is_root = os.geteuid() == 0 if hasattr(os, 'geteuid') else False
                
                if not is_root:
                    self.net_cond_result_text.insert(tk.END, "Uyarı: Bu komutun çalışması için root yetkileri gereklidir!\n")
                    self.net_cond_result_text.insert(tk.END, "Aşağıdaki komutu sudo ile çalıştırın:\n\n")
                
                # tc komutlarını oluştur
                # 1. Önceki kuralları temizle
                clean_cmd = ["tc", "qdisc", "del", "dev", interface, "root"]
                
                # 2. Yeni kuralları ekle
                netem_cmd = ["tc", "qdisc", "add", "dev", interface, "root", "netem"]
                
                # Gecikme ekle
                if delay > 0:
                    netem_cmd.extend(["delay", f"{delay}ms"])
                    if jitter > 0:
                        netem_cmd.extend([f"{jitter}ms", "distribution", "normal"])
                
                # Paket kaybı ekle
                if packet_loss > 0:
                    netem_cmd.extend(["loss", f"{packet_loss}%"])
                
                # Bant genişliği kısıtlaması ekle
                if bandwidth > 0:
                    # Eğer bandwidth sınırlaması var, netem'den sonra tbf ekle
                    tbf_cmd = ["tc", "qdisc", "add", "dev", interface, "root", "tbf", 
                              "rate", f"{bandwidth}kbit", "burst", "32kbit", "latency", "400ms"]
                
                # Komut satırını göster
                self.net_cond_result_text.insert(tk.END, "\nTemizleme komutu:\n")
                self.net_cond_result_text.insert(tk.END, f"sudo {' '.join(clean_cmd)}\n\n")
                
                self.net_cond_result_text.insert(tk.END, "Koşullar komutu:\n")
                self.net_cond_result_text.insert(tk.END, f"sudo {' '.join(netem_cmd)}\n\n")
                
                if bandwidth > 0:
                    self.net_cond_result_text.insert(tk.END, "Bant genişliği komutu:\n")
                    self.net_cond_result_text.insert(tk.END, f"sudo {' '.join(tbf_cmd)}\n\n")
                
                # Yetkimiz varsa komutları çalıştır
                if is_root:
                    try:
                        # Önce temizleme komutunu çalıştır (hata görmezden gelinebilir)
                        subprocess.run(clean_cmd, stderr=subprocess.PIPE)
                        
                        # Sonra netem komutunu çalıştır
                        netem_result = subprocess.run(netem_cmd, stderr=subprocess.PIPE, text=True)
                        
                        if netem_result.returncode == 0:
                            self.net_cond_result_text.insert(tk.END, "Netem kuralları başarıyla uygulandı.\n")
                            
                            # Bant genişliği sınırlaması ekle
                            if bandwidth > 0:
                                tbf_result = subprocess.run(tbf_cmd, stderr=subprocess.PIPE, text=True)
                                if tbf_result.returncode == 0:
                                    self.net_cond_result_text.insert(tk.END, "Bant genişliği kuralları başarıyla uygulandı.\n")
                                else:
                                    self.net_cond_result_text.insert(tk.END, f"Bant genişliği kuralları uygulanırken hata: {tbf_result.stderr}\n")
                        else:
                            self.net_cond_result_text.insert(tk.END, f"Netem kuralları uygulanırken hata: {netem_result.stderr}\n")
                            
                    except Exception as e:
                        self.net_cond_result_text.insert(tk.END, f"Komut çalıştırılırken hata: {str(e)}\n")
                else:
                    self.net_cond_result_text.insert(tk.END, "\nLütfen yukarıdaki komutları terminalde root yetkileriyle çalıştırın.\n")
                
            except Exception as e:
                self.net_cond_result_text.insert(tk.END, f"Ağ koşullarını uygularken hata: {str(e)}\n")
        
        # Thread'i başlat ve referansını tut
        self.network_condition_thread = threading.Thread(target=run_apply_conditions, daemon=True)
        self.network_condition_thread.start()
    
    def reset_network_conditions(self):
        """Ağ koşullarını sıfırlar (tüm kuralları kaldırır)"""
        interface = self.interface_entry.get()
        
        # Sonuç alanını temizle
        self.net_cond_result_text.delete(1.0, tk.END)
        self.net_cond_result_text.insert(tk.END, f"{interface} arayüzündeki ağ koşulları sıfırlanıyor...\n")
        
        def run_reset_conditions():
            try:
                import platform
                import subprocess
                import os
                
                os_name = platform.system()
                
                if os_name != "Linux":
                    self.net_cond_result_text.insert(tk.END, "Bu özellik yalnızca Linux'ta desteklenmektedir.\n")
                    self.net_cond_result_text.insert(tk.END, "Diğer işletim sistemleri için Charles Proxy veya Fiddler kullanabilirsiniz.\n")
                    return
                
                # Root yetkisi kontrol et
                is_root = os.geteuid() == 0 if hasattr(os, 'geteuid') else False
                
                if not is_root:
                    self.net_cond_result_text.insert(tk.END, "Uyarı: Bu komutun çalışması için root yetkileri gereklidir!\n")
                    self.net_cond_result_text.insert(tk.END, "Aşağıdaki komutu sudo ile çalıştırın:\n\n")
                
                # tc komutunu oluştur
                cmd = ["tc", "qdisc", "del", "dev", interface, "root"]
                
                # Komut satırını göster
                self.net_cond_result_text.insert(tk.END, f"sudo {' '.join(cmd)}\n\n")
                
                # Yetkimiz varsa komutu çalıştır
                if is_root:
                    try:
                        result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
                        
                        # RTNETLINK hatası qdisc bulunamadı hatasıdır - bu zaten temiz olduğu anlamına gelir
                        if result.returncode == 0 or "RTNETLINK answers: No such file or directory" in result.stderr:
                            self.net_cond_result_text.insert(tk.END, "Ağ koşulları başarıyla sıfırlandı.\n")
                        else:
                            self.net_cond_result_text.insert(tk.END, f"Ağ koşulları sıfırlanırken hata: {result.stderr}\n")
                    
                    except Exception as e:
                        self.net_cond_result_text.insert(tk.END, f"Komut çalıştırılırken hata: {str(e)}\n")
                else:
                    self.net_cond_result_text.insert(tk.END, "Lütfen yukarıdaki komutu terminalde root yetkileriyle çalıştırın.\n")
                
            except Exception as e:
                self.net_cond_result_text.insert(tk.END, f"Ağ koşullarını sıfırlarken hata: {str(e)}\n")
        
        # Thread'i başlat ve referansını tut
        self.network_condition_thread = threading.Thread(target=run_reset_conditions, daemon=True)
        self.network_condition_thread.start()
    
    def test_network_conditions(self):
        """Mevcut ağ koşullarını ping testi ile test eder"""
        target = "8.8.8.8"  # Google DNS - çoğu sistemde erişilebilir
        count = 5  # Gönderilecek ping sayısı
        
        # Sonuç alanını temizle
        self.net_cond_result_text.delete(1.0, tk.END)
        self.net_cond_result_text.insert(tk.END, f"{target} adresine ping testi başlatılıyor...\n")
        self.net_cond_result_text.insert(tk.END, f"Bu test, uygulanan ağ koşullarının etkilerini gösterecek.\n\n")
        
        def run_test():
            try:
                from scapy.all import IP, ICMP, sr1
                import time
                import statistics
                
                results = []
                lost_packets = 0
                
                for i in range(count):
                    start_time = time.time()
                    
                    try:
                        self.net_cond_result_text.insert(tk.END, f"Ping {i+1} gönderiliyor... ")
                        response = sr1(IP(dst=target)/ICMP(), timeout=5, verbose=0)
                        
                        if response:
                            rtt = (time.time() - start_time) * 1000  # ms cinsinden
                            results.append(rtt)
                            self.net_cond_result_text.insert(tk.END, f"RTT: {rtt:.2f} ms\n")
                        else:
                            self.net_cond_result_text.insert(tk.END, "Yanıt yok (zaman aşımı)\n")
                            lost_packets += 1
                    except Exception as e:
                        self.net_cond_result_text.insert(tk.END, f"Hata: {str(e)}\n")
                        lost_packets += 1
                    
                    # Kısa süre bekle
                    time.sleep(0.5)
                
                # İstatistikleri göster
                self.net_cond_result_text.insert(tk.END, "\nSonuçlar:\n")
                self.net_cond_result_text.insert(tk.END, f"  Gönderilen ping sayısı: {count}\n")
                self.net_cond_result_text.insert(tk.END, f"  Alınan yanıt sayısı: {count - lost_packets}\n")
                self.net_cond_result_text.insert(tk.END, f"  Paket kaybı oranı: {(lost_packets / count) * 100:.1f}%\n")
                
                if results:
                    min_rtt = min(results)
                    max_rtt = max(results)
                    avg_rtt = sum(results) / len(results)
                    
                    self.net_cond_result_text.insert(tk.END, f"  Minimum RTT: {min_rtt:.2f} ms\n")
                    self.net_cond_result_text.insert(tk.END, f"  Maksimum RTT: {max_rtt:.2f} ms\n")
                    self.net_cond_result_text.insert(tk.END, f"  Ortalama RTT: {avg_rtt:.2f} ms\n")
                    
                    if len(results) > 1:
                        std_dev = statistics.stdev(results)
                        self.net_cond_result_text.insert(tk.END, f"  Standart sapma: {std_dev:.2f} ms\n")
                
                # Yorumla
                self.net_cond_result_text.insert(tk.END, "\nYorum:\n")
                if lost_packets > 0:
                    self.net_cond_result_text.insert(tk.END, "  Paket kaybı tespit edildi. Ağ koşulları simülasyonu çalışıyor olabilir.\n")
                
                if results:
                    if max_rtt - min_rtt > 50:
                        self.net_cond_result_text.insert(tk.END, "  Yüksek RTT değişkenliği tespit edildi. Gecikme simülasyonu çalışıyor olabilir.\n")
                    if avg_rtt > 200:
                        self.net_cond_result_text.insert(tk.END, "  Yüksek ortalama RTT tespit edildi. Gecikme simülasyonu çalışıyor olabilir.\n")
                
            except Exception as e:
                self.net_cond_result_text.insert(tk.END, f"\nTest sırasında hata: {str(e)}\n")
        
        # Thread'i başlat ve referansını tut
        self.test_thread = threading.Thread(target=run_test, daemon=True)
        self.test_thread.start()
        
        def run_list_interfaces():
            try:
                import platform
                import subprocess
                import re
                
                os_name = platform.system()
                
                if os_name == "Linux":
                    # Linux için ip komutunu kullan
                    cmd = ["ip", "link", "show"]
                    self.net_cond_result_text.insert(tk.END, "Linux ağ arayüzleri:\n")
                elif os_name == "Darwin":  # macOS
                    # macOS için ifconfig komutunu kullan
                    cmd = ["ifconfig"]
                    self.net_cond_result_text.insert(tk.END, "macOS ağ arayüzleri:\n")
                elif os_name == "Windows":
                    # Windows için ipconfig kullan
                    cmd = ["ipconfig"]
                    self.net_cond_result_text.insert(tk.END, "Windows ağ arayüzleri:\n")
                else:
                    self.net_cond_result_text.insert(tk.END, f"Desteklenmeyen işletim sistemi: {os_name}\n")
                    return
                
                # Komutu çalıştır
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate()
                
                if process.returncode == 0:
                    # Komut başarılı olduğunda çıktısını göster
                    self.net_cond_result_text.insert(tk.END, stdout)
                    
                    # Önerilen arayüz adını tespit etmeye çalış
                    if os_name == "Linux":
                        # Linux'ta eth0, enp0s3 gibi isimleri ara
                        interfaces = re.findall(r'\d+: ([\w]+):', stdout)
                        if interfaces:
                            # İlk arayüzü öner (lo harioç)
                            for interface in interfaces:
                                if interface != "lo":
                                    self.interface_entry.delete(0, tk.END)
                                    self.interface_entry.insert(0, interface)
                                    self.net_cond_result_text.insert(tk.END, f"\nÖnerilen arayüz: {interface}\n")
                                    break
                    elif os_name == "Darwin":  # macOS
                        # en0, en1 gibi arayüzleri ara
                        interfaces = re.findall(r'^([\w\d]+):', stdout, re.MULTILINE)
                        if interfaces:
                            # en0 veya diğer fiziksel arayüzleri öner (lo0 hariç)
                            for interface in interfaces:
                                if interface != "lo0":
                                    self.interface_entry.delete(0, tk.END)
                                    self.interface_entry.insert(0, interface)
                                    self.net_cond_result_text.insert(tk.END, f"\nÖnerilen arayüz: {interface}\n")
                                    break
                                    
                else:
                    # Hata durumunda hata mesajını göster
                    self.net_cond_result_text.insert(tk.END, f"Hata oluştu (kod: {process.returncode}):\n")
                    self.net_cond_result_text.insert(tk.END, stderr)
                    
            except Exception as e:
                self.net_cond_result_text.insert(tk.END, f"Ağ arayüzlerini listelerken hata: {str(e)}\n")
        
        # Thread'i başlat
        threading.Thread(target=run_list_interfaces, daemon=True).start()
        
        def run_install():
            try:
                import shutil
                import subprocess
                import platform
                
                # iPerf3'ün kurulu olup olmadığını kontrol et
                iperf3_path = shutil.which("iperf3")
                
                if iperf3_path:
                    self.bw_result_text.insert(tk.END, f"\niPerf3 zaten kurulu: {iperf3_path}\n")
                    return
                
                # İşletim sistemini tespit et ve kurulum komutunu belirle
                os_name = platform.system()
                
                if os_name == "Darwin":  # macOS
                    cmd = ["brew", "install", "iperf3"]
                    self.bw_result_text.insert(tk.END, "macOS için Homebrew ile iPerf3 kuruluyor...\n")
                elif os_name == "Linux":
                    # Ubuntu, Debian vb. için apt
                    cmd = ["apt-get", "update", "&&", "apt-get", "install", "-y", "iperf3"]
                    self.bw_result_text.insert(tk.END, "Linux için apt ile iPerf3 kuruluyor...\n")
                    
                    # Not: Burada dağıtıma göre farklı komutlar eklenebilir (yum, dnf vb.)
                elif os_name == "Windows":
                    self.bw_result_text.insert(tk.END, "Windows için lütfen iPerf3'ü manuel olarak indiriniz:\n")
                    self.bw_result_text.insert(tk.END, "https://iperf.fr/iperf-download.php\n")
                    return
                else:
                    self.bw_result_text.insert(tk.END, f"Desteklenmeyen işletim sistemi: {os_name}\n")
                    return
                
                # Kurulum komutunu çalıştır
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate()
                
                # Sonuçları göster
                if process.returncode == 0:
                    self.bw_result_text.insert(tk.END, "\niPerf3 başarıyla kuruldu!\n")
                else:
                    self.bw_result_text.insert(tk.END, f"\niPerf3 kurulumu sırasında hata oluştu (kod: {process.returncode}):\n")
                    self.bw_result_text.insert(tk.END, stderr)
                    
                    # Alternatif kurulum yolunu öner
                    self.bw_result_text.insert(tk.END, "\nLütfen iPerf3'ü manuel olarak kurunuz:\n")
                    self.bw_result_text.insert(tk.END, "https://iperf.fr/iperf-download.php\n")
                
            except Exception as e:
                self.bw_result_text.insert(tk.END, f"\niPerf3 kurulumu sırasında hata: {str(e)}\n")
    
    def start_ping_test(self):
        """Ping testi başlatır"""
        target = self.ping_target_entry.get()
        
        try:
            count = int(self.ping_count_spinbox.get())
        except ValueError:
            messagebox.showerror("Hata", "Ping sayısı geçerli bir sayı olmalıdır!")
            return
        
        # Metin alanını temizle
        self.ping_result_text.delete(1.0, tk.END)
        self.ping_result_text.insert(tk.END, f"{target} adresine ping testi başlatılıyor...\n")
        
        # Grafik alanını temizle (eğer varsa)
        if MATPLOTLIB_AVAILABLE:
            self.ping_data = []
            self.ping_ax.clear()
            self.ping_ax.set_title("RTT Ölçüm Sonuçları")
            self.ping_ax.set_xlabel("Ping Sırası")
            self.ping_ax.set_ylabel("RTT (ms)")
        
        # Test butonunu devre dışı bırak
        self.start_ping_btn["state"] = "disabled"
        
        # Ping testini arka planda çalıştır
        def run_ping_test_thread():
            try:
                results_list = []
                
                for i in range(count):
                    start_time = time.time()
                    
                    try:
                        from scapy.all import IP, ICMP, sr1
                        
                        # ICMP echo request gönder
                        response = sr1(IP(dst=target)/ICMP(), timeout=2, verbose=0)
                        
                        if response:
                            rtt = (time.time() - start_time) * 1000  # ms cinsinden
                            status = "Başarılı"
                            results_list.append(rtt)
                            
                            # Metin alanına ekle
                            self.ping_result_text.insert(tk.END, f"Ping {i+1}: {rtt:.2f} ms\n")
                            
                            # Grafiğe ekle (eğer varsa) - thread-safe şekilde güncelle
                            if MATPLOTLIB_AVAILABLE:
                                self.ping_data.append(rtt)
                                # Thread güvenli şekilde GUI güncellemesi yap
                                indices = list(range(1, len(self.ping_data) + 1))
                                current_data = self.ping_data.copy()  # Veri kopyasını al
                                
                                # Ana thread'de çalıştır
                                self.root.after(0, lambda: self._update_ping_graph(current_data, indices))
                        else:
                            self.ping_result_text.insert(tk.END, f"Ping {i+1}: Yanıt yok (zaman aşımı)\n")
                            status = "Başarısız (Yanıt yok)"
                    except Exception as e:
                        self.ping_result_text.insert(tk.END, f"Ping {i+1}: Hata - {str(e)}\n")
                        status = f"Hata: {str(e)}"
                    
                    # Thread'i kısa süre beklet
                    time.sleep(0.5)
                
                # İstatistikleri göster
                if results_list:
                    import statistics
                    
                    min_rtt = min(results_list)
                    max_rtt = max(results_list)
                    avg_rtt = statistics.mean(results_list)
                    
                    self.ping_result_text.insert(tk.END, "\nİstatistikler:\n")
                    self.ping_result_text.insert(tk.END, f"  Gönderilen ping sayısı: {count}\n")
                    self.ping_result_text.insert(tk.END, f"  Alınan yanıt sayısı: {len(results_list)}\n")
                    self.ping_result_text.insert(tk.END, f"  Paket kaybı: {(count - len(results_list)) / count * 100:.1f}%\n")
                    self.ping_result_text.insert(tk.END, f"  Minimum RTT: {min_rtt:.2f} ms\n")
                    self.ping_result_text.insert(tk.END, f"  Maksimum RTT: {max_rtt:.2f} ms\n")
                    self.ping_result_text.insert(tk.END, f"  Ortalama RTT: {avg_rtt:.2f} ms\n")
                    
                    if len(results_list) > 1:
                        self.ping_result_text.insert(tk.END, f"  Standart sapma: {statistics.stdev(results_list):.2f} ms\n")
                else:
                    self.ping_result_text.insert(tk.END, "\nHiçbir ping yanıtı alınmadı.\n")
                
            except Exception as e:
                self.ping_result_text.insert(tk.END, f"\nPing işlemi sırasında hata: {str(e)}\n")
            finally:
                # Test butonunu tekrar aktif et
                self.start_ping_btn["state"] = "normal"
        
        # Thread'i başlat ve referansını tut
        self.ping_thread = threading.Thread(target=run_ping_test_thread, daemon=True)
        self.ping_thread.start()
    
    def return_to_main_menu(self):
        """Ana menüye geri dön
        
        Güvenli şekilde tüm thread'leri sonlandırır ve kaynakları serbest bırakır.
        """
        # Önce tüm thread'leri sonlandır
        self.running = False
        
        print("[*] Thread'ler güvenli bir şekilde sonlandırılıyor...")
        time.sleep(0.5)  # Thread'lere sonlanma şansı ver
        
        # Ping testi ve bant genişliği testi threadlerini kontrol et ve beklet
        if self.bandwidth_thread and self.bandwidth_thread.is_alive():
            try:
                self.bandwidth_thread.join(1.0)  # En fazla 1 saniye bekle
            except:
                pass
                
        if self.ping_thread and self.ping_thread.is_alive():
            try:
                self.ping_thread.join(1.0)
            except:
                pass
                
        if self.test_thread and self.test_thread.is_alive():
            try:
                self.test_thread.join(1.0)
            except:
                pass
                
        if self.network_condition_thread and self.network_condition_thread.is_alive():
            try:
                self.network_condition_thread.join(1.0)
            except:
                pass
                
        # Çalışan process'leri sonlandırmaya çalış (Linux'ta)
        try:
            if platform.system() == "Linux":
                os.system("pkill -f iperf3 &>/dev/null || true")
        except:
            pass
                
        # Pencereyi kapat ve ana menüye dön
        self.root.destroy()
        from src.gui.app import main
        main()
    
    def _update_ping_graph(self, data, indices):
        """Ping grafiğini thread-safe bir şekilde günceller"""
        if MATPLOTLIB_AVAILABLE:
            try:
                self.ping_ax.clear()
                self.ping_ax.plot(indices, data, 'bo-')
                self.ping_ax.set_title("RTT Ölçüm Sonuçları")
                self.ping_ax.set_xlabel("Ping Sırası")
                self.ping_ax.set_ylabel("RTT (ms)")
                self.ping_canvas.draw()
            except Exception as e:
                print(f"[!] Grafik güncellenirken hata oluştu: {str(e)}")
    
    def run(self):
        """GUI döngüsünü çalıştır"""
        self.root.mainloop()

# Ana fonksiyon
def run_network_analysis_gui():
    """Ağ analiz GUI'sini başlatır"""
    app = NetworkAnalysisGUI()
    app.run()

if __name__ == "__main__":
    run_network_analysis_gui()
