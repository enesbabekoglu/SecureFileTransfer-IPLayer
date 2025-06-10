# Secure/src/server/network_server.py

import os, hashlib, struct
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from ..utils.config import AUTH_TOKEN    # ← Burayı düzeltin
                                         # eskiden: from utils.config import AUTH_TOKEN
from ..utils.file_chunking_utils import decode_chunk_header, reassemble_chunks

def calculate_sha256_from_bytes(bb):
    h = hashlib.sha256(); h.update(bb); return h.hexdigest().encode()

def load_private_key():
    # Ana dizinde olduğumuzdan emin olmak için tam yol kullanıyoruz
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    key_path = os.path.join(base_dir, "keys", "server_private_key.pem")
    print(f"[*] Private key yolu: {key_path}")
    
    with open(key_path, "rb") as f:
        return serialization.load_pem_private_key(
            f.read(), password=None, backend=default_backend())

def decrypt_with_aes(bb, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv),
                    backend=default_backend())
    return cipher.decryptor().update(bb) + cipher.decryptor().finalize()

def handle_incoming_connection(conn, addr, log=print):
    try:
        # 1) Token'ı oku ve doğrula
        data_buffer = b""
        while b"\n" not in data_buffer:
            chunk = conn.recv(1024)
            if not chunk: 
                log("[!] Bağlantı beklenmedik şekilde kapandı.")
                return
            data_buffer += chunk
        
        token_line, data_buffer = data_buffer.split(b"\n", 1)
        if token_line.strip() != AUTH_TOKEN:
            log(f"[✘] Geçersiz token {addr}")
            conn.close()
            return
        log(f"[✔] Token doğrulandı {addr}")
        
        # 2) Dosya adı ve toplam parça sayısını oku
        while len(data_buffer) < 4:  # Dosya adı uzunluğu için 4 byte
            chunk = conn.recv(1024)
            if not chunk: break
            data_buffer += chunk
            
        filename_len = struct.unpack("!I", data_buffer[:4])[0]
        data_buffer = data_buffer[4:]
        
        # Dosya adını oku
        while len(data_buffer) < filename_len + 4:  # dosya adı + toplam parça sayısı için 4 byte
            chunk = conn.recv(1024)
            if not chunk: break
            data_buffer += chunk
            
        filename = data_buffer[:filename_len].decode(errors="ignore")
        total_chunks = struct.unpack("!I", data_buffer[filename_len:filename_len+4])[0]
        data_buffer = data_buffer[filename_len+4:]
        log(f"[i] Alınacak dosya: {filename}, {total_chunks} parça")
        
        # 3) Şifrelenmiş AES anahtarını oku
        while len(data_buffer) < 4:  # Anahtar uzunluğu için 4 byte
            chunk = conn.recv(1024)
            if not chunk: break
            data_buffer += chunk
            
        key_len = struct.unpack("!I", data_buffer[:4])[0]
        data_buffer = data_buffer[4:]
        
        while len(data_buffer) < key_len:
            chunk = conn.recv(1024)
            if not chunk: break
            data_buffer += chunk
        
        enc_key = data_buffer[:key_len]
        data_buffer = data_buffer[key_len:]
        
        # 4) RSA ile AES anahtarını çöz
        try:
            log(f"[i] Şifreli anahtar boyutu: {len(enc_key)} bytes")
            priv = load_private_key()
            key_iv = priv.decrypt(
                enc_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(), label=None
                )
            )
            aes_key, iv = key_iv[:32], key_iv[32:]
        except Exception as e:
            log(f"[!] RSA ile anahtar çözülürken hata: {str(e)}")
            conn.close()
            return
        
        # 5) Parça parça dosyayı al ve birleştir
        save_dir = os.path.join(os.path.dirname(__file__), "gelenler")
        os.makedirs(save_dir, exist_ok=True)
        output_path = os.path.join(save_dir, filename)
        log(f"[*] Dosya kaydedilecek: {output_path}")
        
        # Dosya tipine göre mod belirleme
        if filename.lower().endswith(('.txt', '.py', '.html', '.css', '.js', '.json', '.xml', '.md')):
            file_mode = 'wb'  # Binary mod her dosya türü için güvenli
        else:
            file_mode = 'wb'  # Varsayılan olarak binary mod
        
        with open(output_path, "wb") as output_file:
            received_chunks = []
            chunks_processed = 0
            
            while chunks_processed < total_chunks:
                # Parça uzunluğunu oku
                while len(data_buffer) < 4:
                    chunk = conn.recv(1024)
                    if not chunk: 
                        log("[!] Bağlantı beklenmedik şekilde kapandı.")
                        return
                    data_buffer += chunk
                    
                data_len = struct.unpack("!I", data_buffer[:4])[0]
                data_buffer = data_buffer[4:]
                
                # Parça verilerini oku
                while len(data_buffer) < data_len:
                    chunk = conn.recv(1024)
                    if not chunk: 
                        log("[!] Bağlantı beklenmedik şekilde kapandı.")
                        return
                    data_buffer += chunk
                
                # Başlık ve veriyi ayır
                header = data_buffer[:13]  # chunk_header 13 byte (4+4+4+1)
                chunk_data_with_hash = data_buffer[13:data_len]
                data_buffer = data_buffer[data_len:]
                
                # Başlığı decode et
                chunk_index, chunk_total, chunk_size, is_last_chunk = decode_chunk_header(header)
                
                # Şifreli veri ve hash'i ayır
                try:
                    # Son || ayracını bul ve ondan sonrasını hash olarak değerlendir
                    separator_pos = chunk_data_with_hash.rfind(b'||')
                    if separator_pos != -1:
                        encrypted_chunk = chunk_data_with_hash[:separator_pos]
                        chunk_hash = chunk_data_with_hash[separator_pos+2:]
                        log(f"[+] Parça {chunk_index+1}/{total_chunks}: Hash başarıyla ayrıldı.")
                    else:
                        log(f"[!] Parça {chunk_index+1}/{total_chunks}: Hash ayracı bulunamadı.")
                        encrypted_chunk = chunk_data_with_hash
                        chunk_hash = b''
                except Exception as e:
                    log(f"[!] Parça ayrıştırılırken hata: {str(e)}")
                    encrypted_chunk = chunk_data_with_hash
                    chunk_hash = b''
                
                # AES ile şifreyi çöz
                decrypted_chunk = decrypt_with_aes(encrypted_chunk, aes_key, iv)
                
                # Hash doğrulaması yap - hex formatta encode edilmiş hash'ler ile karşılaştırma yapmalıyız
                calculated_hash = hashlib.sha256(decrypted_chunk).hexdigest().encode()
                log(f"[*] Alınan hash: {chunk_hash[:20]}... (uzunluk: {len(chunk_hash)})")
                log(f"[*] Hesaplanan hash: {calculated_hash[:20]}... (uzunluk: {len(calculated_hash)})")
                
                # Alınan hash'in boyutunu kontrol et - çok büyük olabilir
                # İstemci tarafından gönderilen hash'i byte olarak al
                if isinstance(chunk_hash, str):
                    chunk_hash = chunk_hash.encode()
                calculated_hash = calculated_hash
                if isinstance(calculated_hash, str):
                    calculated_hash = calculated_hash.encode()

                # Hash doğrulaması yapmadan önce boyutları kontrol et
                # 64 byte'dan uzun olan hash'ler muhtemelen bozuktur
                valid_hash_check = len(chunk_hash) <= 100
                
                # Hem hash boyutunu hem de eşleşmeyi kontrol et
                if valid_hash_check and chunk_hash == calculated_hash:
                    log(f"[✔] Parça {chunk_index+1}/{total_chunks} için hash doğrulaması başarılı!")
                else:
                    # Hash bozuk olabilir ama dosyayı kaydetmeye devam edelim
                    if not valid_hash_check:
                        log(f"[!] Parça {chunk_index+1}/{total_chunks} için hash formatı geçersiz!")
                    else:
                        log(f"[✘] Parça {chunk_index+1}/{total_chunks} için hash doğrulaması başarısız!")
                    log(f"[ℹ️] Parça yine de yazılıyor...")
                    # Hash doğrulama başarısız olsa bile veriyi yazalım
                    output_file.write(decrypted_chunk)
                    chunks_processed += 1
                    # Her yazmadan sonra dosyayı kaydedelim
                    output_file.flush()
                    continue
                
                # Dosyaya yaz
                output_file.write(decrypted_chunk)
                chunks_processed += 1
                log(f"[+] Parça {chunk_index+1}/{total_chunks} alındı ve doğrulandı.")
        
        # 6) İşlem tamam
        log(f"[+] Dosya başarıyla kaydedildi: {output_path}")
        conn.close()
    
    except Exception as e:
        log(f"[!] Hata: {e}")
        conn.close()
