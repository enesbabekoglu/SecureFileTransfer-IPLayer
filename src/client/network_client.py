import socket
import os
import struct
from utils.config import SERVER_IP, SERVER_PORT, AUTH_TOKEN, PUBLIC_KEY_PATH
from utils.file_utils import read_file_bytes, calculate_sha256
from utils.cryptography_utils import generate_aes_key_iv, encrypt_with_aes, encrypt_key_with_rsa
from utils.file_chunking_utils import chunk_file_generator, create_chunk_header, DEFAULT_CHUNK_SIZE

def send_file(filepath: str, chunk_size: int = DEFAULT_CHUNK_SIZE) -> str:
    """
    Dosyayı parçalar halinde gönder
    
    Args:
        filepath: Gönderilecek dosyanın yolu
        chunk_size: Parça boyutu (byte)
        
    Returns:
        str: İşlem sonucu mesajı
    """
    try:
        # 1. AES key & IV oluştur (tüm parçalar için aynı anahtar kullanacağız)
        aes_key, iv = generate_aes_key_iv()
        
        # 2. AES key + IV'yi birleştirip RSA ile şifrele
        encrypted_key = encrypt_key_with_rsa(PUBLIC_KEY_PATH, aes_key + iv)
        
        # 3. Dosya boyutunu al ve toplam parça sayısını hesapla
        filesize = os.path.getsize(filepath)
        total_chunks = (filesize + chunk_size - 1) // chunk_size  # Yukarı yuvarlama
        
        # 4. Socket ile sunucuya bağlan
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((SERVER_IP, SERVER_PORT))
            
            # 5. Token gönder
            sock.sendall(AUTH_TOKEN + b"\n")
            
            # 6. Dosya adını ve toplam parça sayısını gönder
            filename = os.path.basename(filepath).encode()
            file_info = struct.pack("!I", len(filename)) + filename + struct.pack("!I", total_chunks)
            sock.sendall(file_info)
            
            # 7. Şifrelenmiş anahtarı gönder
            key_len_bytes = struct.pack("!I", len(encrypted_key))
            sock.sendall(key_len_bytes + encrypted_key)
            
            # 8. Dosyayı parçalar halinde gönder
            for i, (chunk_data, chunk_hash) in enumerate(chunk_file_generator(filepath, chunk_size)):
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
                
                # 8.3. Parça hash'ini ekle
                chunk_data_with_hash = encrypted_chunk + b'||' + chunk_hash
                
                # 8.4. Parça uzunluğunu ve içeriğini gönder
                data_len_bytes = struct.pack("!I", len(header) + len(chunk_data_with_hash))
                sock.sendall(data_len_bytes + header + chunk_data_with_hash)
                
                print(f"[+] Parça {i+1}/{total_chunks} gönderildi. Boyut: {len(chunk_data)} bytes")
        
        return "Dosya parçalar halinde başarıyla gönderildi."
    except Exception as e:
        return f"Dosya gönderirken hata oluştu: {str(e)}"
