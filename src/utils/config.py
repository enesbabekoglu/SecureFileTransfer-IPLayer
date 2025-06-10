# secure_gui/config.py
import os

SERVER_IP = "127.0.0.1"
SERVER_PORT = 10000
AUTH_TOKEN = b"gizli_token_123"

# Projenin ana dizinini bulma
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Public key için tam yol oluşturma
PUBLIC_KEY_PATH = os.path.join(BASE_DIR, "keys", "server_public_key.pem")