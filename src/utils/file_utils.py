# secure_gui/file_utils.py

import hashlib

def calculate_sha256(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest().encode()

def read_file_bytes(file_path):
    with open(file_path, "rb") as f:
        return f.read()