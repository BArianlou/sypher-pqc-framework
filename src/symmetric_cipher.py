from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag
import os

class SypherCipher:
    """Authenticated Encryption with Associated Data (AEAD) via AES-256-GCM."""
    def __init__(self, shared_secret: bytes):
        # Triune Architect Check: Ensure exact 256-bit key
        if len(shared_secret) != 32:
            raise ValueError("SypherCipher requires a 256-bit (32-byte) shared secret.")
        self.key = shared_secret
        self.aesgcm = AESGCM(self.key)

    def encrypt(self, plaintext: str, associated_data: bytes = None) -> bytes:
        nonce = os.urandom(12)
        # Ge's explicit utf-8 encoding + Triune's AAD support
        ciphertext = self.aesgcm.encrypt(nonce, plaintext.encode('utf-8'), associated_data)
        return nonce + ciphertext

    def decrypt(self, encrypted_payload: bytes, associated_data: bytes = None) -> str:
        # Ge's defensive payload length check
        if len(encrypted_payload) < 12:
            raise ValueError("Payload too short to contain valid GCM nonce.")
            
        nonce = encrypted_payload[:12]
        ciphertext = encrypted_payload[12:]
        
        try:
            # Triune's AAD verification
            plaintext = self.aesgcm.decrypt(nonce, ciphertext, associated_data)
            # Ge's explicit utf-8 decoding
            return plaintext.decode('utf-8')
        except InvalidTag:
            raise ValueError("SYPHER INTEGRITY FATAL: Authentication tag verification failed. Payload modified or corrupted.")
