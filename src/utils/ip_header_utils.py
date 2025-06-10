#!/usr/bin/env python3
"""
IP Başlık İşleme Modülü - Düşük seviyeli IP başlık manipülasyonu için kullanılır.
"""
import os
import sys
from scapy.all import IP, ICMP, TCP, UDP, send, sr, sr1, fragment

def create_custom_ip_packet(dst_ip, src_ip=None, ttl=64, flags="DF", frag=0):
    """
    Özel IP başlık ayarları ile paket oluşturur
    
    Parametreler:
    - dst_ip: Hedef IP adresi
    - src_ip: Kaynak IP adresi (None ise otomatik)
    - ttl: Time To Live değeri
    - flags: IP bayrakları (DF=Don't Fragment, MF=More Fragments)
    - frag: Fragment offset değeri
    """
    ip_packet = IP(dst=dst_ip, src=src_ip, ttl=ttl, flags=flags, frag=frag)
    return ip_packet

def calculate_ip_checksum(packet):
    """
    IP paketi için checksum hesaplar
    """
    # Scapy, gönderilmeden önce checksum'ı otomatik hesaplar
    # Ancak manuel hesaplamak için mevcut checksum'ı sıfırlayalım
    del packet.chksum
    return packet.__class__(bytes(packet)).chksum

def validate_ip_checksum(packet):
    """
    IP paketinin checksum değerini doğrular
    """
    original_chksum = packet.chksum
    del packet.chksum
    calculated_chksum = packet.__class__(bytes(packet)).chksum
    return original_chksum == calculated_chksum

def fragment_and_send(packet, fragment_size=500):
    """
    Büyük bir paketi parçalara ayırır ve gönderir
    
    Parametreler:
    - packet: Parçalanacak IP paketi
    - fragment_size: Her bir parçanın maksimum boyutu (bayt)
    
    Dönüş:
    - Oluşturulan parça listesi
    """
    frags = fragment(packet, fragsize=fragment_size)
    send(frags)
    return frags

def reassemble_fragments(fragments):
    """
    IP paket parçalarını birleştirir
    
    Parametreler:
    - fragments: Birleştirilecek IP paket parçaları listesi
    
    Dönüş:
    - Birleştirilmiş IP paketi
    """
    # Scapy otomatik olarak aynı ID'ye sahip parçaları birleştirmez
    # Bu fonksiyon, manuel olarak parçaları birleştirip orijinal paketi oluşturur
    
    if not fragments:
        return None
    
    # Parçaları ID ve fragmentasyon offset değerine göre sırala
    fragments.sort(key=lambda f: f.frag)
    
    # İlk parça için temel bilgileri al
    base_packet = fragments[0]
    
    # Tüm parçaları birleştir
    payload = b""
    for frag in fragments:
        payload += bytes(frag.payload)
    
    # Yeni birleştirilmiş paket oluştur
    reassembled = IP(
        src=base_packet.src,
        dst=base_packet.dst,
        id=base_packet.id,
        proto=base_packet.proto
    )
    reassembled.load = payload
    
    return reassembled

def analyze_ip_header(packet):
    """
    IP başlığını analiz eder ve bileşenlerini döndürür
    
    Parametreler:
    - packet: Analiz edilecek IP paketi
    
    Dönüş:
    - IP başlık bilgilerini içeren sözlük
    """
    header_info = {
        "version": packet.version,
        "ihl": packet.ihl,
        "tos": packet.tos,
        "len": packet.len,
        "id": packet.id,
        "flags": packet.flags,
        "frag": packet.frag,
        "ttl": packet.ttl,
        "proto": packet.proto,
        "chksum": packet.chksum,
        "src": packet.src,
        "dst": packet.dst,
        "options": getattr(packet, "options", [])
    }
    return header_info
