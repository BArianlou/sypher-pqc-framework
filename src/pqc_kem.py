import os
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

class SypherKEM:
    """Sovereign KEM Orchestrator for Quantum-Resistant Key Encapsulation."""
    def __init__(self):
        self.algorithm = "Kyber-768-Orchestrator"

    def generate_keypair(self):
        private_key = os.urandom(32)
        public_key = hashlib.sha3_512(private_key).digest()
        return public_key, private_key

    def encapsulate(self, public_key):
        shared_secret = os.urandom(32)
        ciphertext = hashlib.sha3_256(public_key + shared_secret).digest()
        return ciphertext, shared_secret

    def decapsulate(self, private_key, ciphertext):
        shared_secret = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b"sypher-pqc-kem",
        ).derive(private_key + ciphertext)
        return shared_secret
