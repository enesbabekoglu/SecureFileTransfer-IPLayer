"""
Büyük dosya transferleri için parçalama ve birleştirme işlevleri.
Bu modül ile büyük dosyalar belirli boyuttaki parçalara ayrılabilir ve alıcı tarafta tekrar birleştirilebilir.
"""

import os
import struct
import hashlib
from typing import List, Tuple, Iterator, BinaryIO

# Varsayılan parça boyutu (1 MB)
DEFAULT_CHUNK_SIZE = 1024 * 1024

def calculate_chunk_hash(chunk_data: bytes) -> bytes:
    """Verilen parça verisi için SHA-256 hash değerini hesaplar."""
    sha256 = hashlib.sha256()
    sha256.update(chunk_data)
    return sha256.hexdigest().encode()

def split_file_into_chunks(file_path: str, chunk_size: int = DEFAULT_CHUNK_SIZE) -> List[Tuple[bytes, bytes]]:
    """
    Dosyayı belirli boyuttaki parçalara ayırır.
    
    Args:
        file_path: Parçalanacak dosyanın yolu
        chunk_size: Her bir parçanın bayt cinsinden boyutu
        
    Returns:
        List[Tuple[bytes, bytes]]: Her parça için (data, hash) çiftlerinin listesi
    """
    chunks = []
    
    with open(file_path, 'rb') as file:
        while True:
            chunk_data = file.read(chunk_size)
            if not chunk_data:
                break
                
            # Her parça için hash değeri hesapla
            chunk_hash = calculate_chunk_hash(chunk_data)
            chunks.append((chunk_data, chunk_hash))
    
    return chunks

def chunk_file_generator(file_path: str, chunk_size: int = DEFAULT_CHUNK_SIZE) -> Iterator[Tuple[bytes, bytes]]:
    """
    Dosyayı belirli boyuttaki parçalara ayırır ve her parçayı yield eder.
    Bu fonksiyon büyük dosyalar için belleği verimli kullanmanızı sağlar.
    
    Args:
        file_path: Parçalanacak dosyanın yolu
        chunk_size: Her bir parçanın bayt cinsinden boyutu
        
    Yields:
        Tuple[bytes, bytes]: Her bir parça için (data, hash) çifti
    """
    with open(file_path, 'rb') as file:
        while True:
            chunk_data = file.read(chunk_size)
            if not chunk_data:
                break
                
            # Her parça için hash değeri hesapla
            chunk_hash = calculate_chunk_hash(chunk_data)
            yield (chunk_data, chunk_hash)

def reassemble_chunks(chunks: List[Tuple[bytes, bytes]], output_file_path: str) -> bool:
    """
    Parçaları birleştirerek orijinal dosyayı oluşturur.
    
    Args:
        chunks: (veri, hash) çiftlerinin listesi
        output_file_path: Çıktı dosyasının yolu
        
    Returns:
        bool: İşlem başarılı olduysa True, başarısız olduysa False
    """
    try:
        # Çıkış dizininin varlığını kontrol et
        output_dir = os.path.dirname(output_file_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        with open(output_file_path, 'wb') as output_file:
            for chunk_data, chunk_hash in chunks:
                # Hash doğrulaması yap
                calculated_hash = calculate_chunk_hash(chunk_data)
                if calculated_hash != chunk_hash:
                    return False
                
                # Parçayı dosyaya yaz
                output_file.write(chunk_data)
        
        return True
    except Exception as e:
        print(f"Parçaları birleştirirken hata oluştu: {e}")
        return False

def reassemble_stream(chunk_stream: Iterator[Tuple[bytes, bytes]], 
                      output_file_handle: BinaryIO) -> bool:
    """
    Parça akışını birleştirerek verilen dosya tanıtıcısına yazar.
    
    Args:
        chunk_stream: (veri, hash) çiftlerinin bir akışı
        output_file_handle: Açık bir dosya nesnesi (write modunda)
        
    Returns:
        bool: İşlem başarılı olduysa True, başarısız olduysa False
    """
    try:
        for chunk_data, chunk_hash in chunk_stream:
            # Hash doğrulaması yap
            calculated_hash = calculate_chunk_hash(chunk_data)
            if calculated_hash != chunk_hash:
                return False
            
            # Parçayı dosyaya yaz
            output_file_handle.write(chunk_data)
        
        return True
    except Exception as e:
        print(f"Parça akışını birleştirirken hata oluştu: {e}")
        return False

def create_chunk_header(chunk_index: int, total_chunks: int, 
                        chunk_size: int, is_last_chunk: bool) -> bytes:
    """
    Parça başlığı oluşturur.
    
    Args:
        chunk_index: Parça indeksi (0-tabanlı)
        total_chunks: Toplam parça sayısı
        chunk_size: Parçanın boyutu (bayt)
        is_last_chunk: Son parça olup olmadığı
        
    Returns:
        bytes: Başlık verisi
    """
    # Format: | chunk_index (4 bytes) | total_chunks (4 bytes) | 
    #         | chunk_size (4 bytes) | is_last_chunk (1 byte) |
    header = struct.pack('!IIIb', chunk_index, total_chunks, chunk_size, 1 if is_last_chunk else 0)
    return header

def decode_chunk_header(header: bytes) -> Tuple[int, int, int, bool]:
    """
    Parça başlığını çözer.
    
    Args:
        header: Başlık verisi
        
    Returns:
        Tuple[int, int, int, bool]: (chunk_index, total_chunks, chunk_size, is_last_chunk)
    """
    chunk_index, total_chunks, chunk_size, is_last = struct.unpack('!IIIb', header)
    return chunk_index, total_chunks, chunk_size, bool(is_last)
