#!/usr/bin/env python3
"""
Ağ Performans Ölçüm Modülü - RTT, bant genişliği ölçümü ve ağ koşulları simülasyonu için kullanılır.
"""
import os
import sys
import time
import socket
import subprocess
import platform
import statistics
import logging
from scapy.all import IP, ICMP, sr1, send

def measure_rtt_ping(target_host, count=5):
    """
    Ping ile RTT (Round Trip Time) ölçümü yapar
    
    Parametreler:
    - target_host: Ping gönderilecek hedef IP adresi
    - count: Gönderilecek ping sayısı
    
    Dönüş:
    - RTT istatistiklerini içeren sözlük
    """
    results = []
    
    # Scapy ile ICMP echo-request gönder
    for i in range(count):
        start_time = time.time()
        reply = sr1(IP(dst=target_host)/ICMP(), timeout=2, verbose=0)
        if reply:
            rtt = (time.time() - start_time) * 1000  # ms cinsinden
            results.append(rtt)
            print(f"Ping {i+1}: {rtt:.2f} ms")
        else:
            print(f"Ping {i+1}: Yanıt yok")
        time.sleep(0.5)
    
    if not results:
        return None
    
    stats = {
        "min": min(results),
        "max": max(results),
        "avg": statistics.mean(results),
        "median": statistics.median(results),
        "stdev": statistics.stdev(results) if len(results) > 1 else 0,
        "packet_loss": (count - len(results)) / count * 100
    }
    
    return stats

def measure_bandwidth_socket(target_host, target_port, duration=5, buffer_size=8192):
    """
    Basit bir socket bağlantısı ile bant genişliği ölçümü
    
    Parametreler:
    - target_host: Hedef sunucu IP adresi
    - target_port: Hedef sunucu port numarası
    - duration: Test süresi (saniye)
    - buffer_size: Gönderilecek veri paketi boyutu (bayt)
    
    Dönüş:
    - Bant genişliği ölçüm sonuçlarını içeren sözlük
    """
    total_bytes = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.connect((target_host, target_port))
        start_time = time.time()
        end_time = start_time + duration
        
        data = b'0' * buffer_size
        
        while time.time() < end_time:
            sock.send(data)
            total_bytes += buffer_size
            
    except Exception as e:
        print(f"Bağlantı hatası: {e}")
    finally:
        sock.close()
    
    actual_duration = time.time() - start_time
    mbps = (total_bytes * 8) / (actual_duration * 1_000_000)
    
    return {
        "bytes_sent": total_bytes,
        "duration": actual_duration,
        "bandwidth_mbps": mbps
    }

def simulate_network_conditions(packet_loss=0, delay_ms=0, bandwidth_limit=None):
    """
    tc ile ağ koşullarını simüle eder (Linux için)
    MacOS ve Windows için proxy tabanlı bir simülasyon alternatif olarak sunulur
    
    Parametreler:
    - packet_loss: Simüle edilecek paket kaybı yüzdesi
    - delay_ms: Simüle edilecek gecikme (milisaniye)
    - bandwidth_limit: Simüle edilecek bant genişliği limiti (kbit/s)
    
    Dönüş:
    - İşlem sonuç bilgisi
    """
    os_name = platform.system()
    
    if os_name == "Linux":
        # Linux için tc kullanımı
        # Ağ arabirimini belirle
        interface = "eth0"  # varsayılan, değiştirilebilir
        
        # Mevcut tc kurallarını temizle
        subprocess.run(f"tc qdisc del dev {interface} root", shell=True)
        
        # Yeni tc kurallarını ekle
        netem_cmd = f"tc qdisc add dev {interface} root netem"
        
        if packet_loss > 0:
            netem_cmd += f" loss {packet_loss}%"
        
        if delay_ms > 0:
            netem_cmd += f" delay {delay_ms}ms"
        
        if bandwidth_limit:
            netem_cmd += f" rate {bandwidth_limit}kbit"
        
        # Komutu çalıştır
        result = subprocess.run(netem_cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            return f"tc komutu çalıştırılamadı: {result.stderr}"
        
        return "Ağ koşul simülasyonu başarıyla uygulandı"
    
    elif os_name == "Darwin" or os_name == "Windows":
        # MacOS veya Windows için
        return "Bu işletim sisteminde ağ koşul simülasyonu için harici bir proxy kullanmanız gerekir. Charles Proxy, Fiddler veya toxiproxy kullanabilirsiniz."
    
    else:
        return "Desteklenmeyen işletim sistemi"

def compare_network_conditions(target_host, tests=None):
    """
    Farklı ağ koşullarını karşılaştırır
    
    Parametreler:
    - target_host: Test edilecek hedef IP adresi
    - tests: Uygulanacak test koşullarının listesi (dict olarak)
    
    Dönüş:
    - Test sonuçlarını içeren sözlük
    """
    if tests is None:
        tests = [
            {"name": "Normal", "packet_loss": 0, "delay_ms": 0},
            {"name": "Yüksek Gecikme", "packet_loss": 0, "delay_ms": 100},
            {"name": "Paket Kaybı", "packet_loss": 5, "delay_ms": 0},
            {"name": "Kötü Bağlantı", "packet_loss": 10, "delay_ms": 200}
        ]
    
    results = {}
    
    for test in tests:
        print(f"Test başlatılıyor: {test['name']}")
        
        # Ağ koşullarını ayarla
        simulate_network_conditions(test["packet_loss"], test["delay_ms"])
        time.sleep(1)  # Ayarların etki etmesi için bekle
        
        # RTT ölçümü
        rtt_results = measure_rtt_ping(target_host)
        
        # Sonuçları kaydet
        results[test["name"]] = {
            "conditions": test,
            "rtt": rtt_results
        }
    
    # Normal duruma geri dön
    simulate_network_conditions()
    
    return results

def run_iperf3_test(server=False, target="localhost", duration=10, port=5201, parallel=4):
    """
    iperf3 ile bant genişliği ölçümü yapar
    
    Parametreler:
    - server: True ise iperf3 sunucu modunda çalıştırılır
    - target: Bağlanılacak iperf3 sunucu adresi (server=False ise)
    - duration: Test süresi (saniye)
    - port: Kullanılacak port numarası
    - parallel: Paralel bağlantı sayısı
    
    Dönüş:
    - iperf3 çıktısı
    """
    try:
        if server:
            cmd = f"iperf3 -s -p {port}"
        else:
            cmd = f"iperf3 -c {target} -t {duration} -p {port} -P {parallel} -J"
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            return f"iperf3 komutu çalıştırılamadı: {result.stderr}"
        
        return result.stdout
    except Exception as e:
        return f"iperf3 testi sırasında hata: {str(e)}"
