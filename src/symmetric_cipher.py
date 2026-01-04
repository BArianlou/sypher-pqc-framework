from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

class SypherCipher:
    """Authenticated Encryption with Associated Data (AEAD) via AES-256-GCM."""
    def __init__(self, shared_secret):
        self.key = shared_secret
        self.aesgcm = AESGCM(self.key)

    def encrypt(self, plaintext):
        nonce = os.urandom(12)
        ciphertext = self.aesgcm.encrypt(nonce, plaintext.encode(), None)
        return nonce + ciphertext

    def decrypt(self, encrypted_payload):
        nonce = encrypted_payload[:12]
        ciphertext = encrypted_payload[12:]
        plaintext = self.aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext.decode()
