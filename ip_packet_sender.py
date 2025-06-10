from scapy.all import IP, TCP, send

# === Ayarlar ===
dst_ip = "127.0.0.1"
dst_port = 12345

# === IP Paketi Oluştur ===
ip = IP(dst=dst_ip, ttl=42, flags='DF')  # Don't Fragment (DF) bayrağı set
tcp = TCP(dport=dst_port, sport=55555, flags='S')  # SYN paketi gönderiyoruz

# === Paketi Gönder ===
packet = ip / tcp
send(packet)

print("[+] Özel IP başlığı ile TCP SYN paketi gönderildi.")
