import socket
import threading
import time

# === Ayarlar ===
LISTEN_HOST = '0.0.0.0'
LISTEN_PORT = 10000          # Proxy üzerinden istemci buraya bağlanacak
DEST_HOST = '127.0.0.1'
DEST_PORT = 12345            # Gerçek sunucu portu
DELAY = 0.1                  # 100 ms gecikme

# === Veri yönlendirici ===
def forward(source, destination, direction="→"):
    while True:
        try:
            data = source.recv(4096)
            if not data:
                break
            time.sleep(DELAY)
            destination.sendall(data)
        except:
            break
    source.close()
    destination.close()

# === Proxy başlat ===
def handle_client(client_socket):
    try:
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((DEST_HOST, DEST_PORT))
    except Exception as e:
        print(f"[!] Sunucuya bağlanılamadı: {e}")
        client_socket.close()
        return

    # Çift yönlü veri aktarımı (gecikmeli)
    threading.Thread(target=forward, args=(client_socket, remote_socket, "→")).start()
    threading.Thread(target=forward, args=(remote_socket, client_socket, "←")).start()

def start_proxy():
    proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy.bind((LISTEN_HOST, LISTEN_PORT))
    proxy.listen(5)
    print(f"[*] Proxy başlatıldı: {LISTEN_HOST}:{LISTEN_PORT} → {DEST_HOST}:{DEST_PORT} (delay: {int(DELAY*1000)}ms)")

    while True:
        client_socket, addr = proxy.accept()
        print(f"[+] Yeni bağlantı: {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_proxy()
