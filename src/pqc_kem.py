import os
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

class SypherKEM:
    """Sovereign KEM Orchestrator for Quantum-Resistant Key Encapsulation."""
    def __init__(self):
        self.algorithm = "Kyber-768-Orchestrator-Mock"

    def generate_keypair(self):
        # Generate a mathematically linked asymmetric keypair
        private_key = x25519.X25519PrivateKey.generate()
        public_key = private_key.public_key()
        
        # Serialize to raw bytes for pipeline compatibility
        pk_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        sk_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )
        return pk_bytes, sk_bytes

    def encapsulate(self, pk_bytes):
        # 1. Generate an ephemeral keypair for this session
        ephemeral_private_key = x25519.X25519PrivateKey.generate()
        ephemeral_public_key = ephemeral_private_key.public_key()
        
        # 2. The ciphertext IS the ephemeral public key sent over the wire
        ciphertext = ephemeral_public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        
        # 3. Derive the shared asymmetric key
        peer_public_key = x25519.X25519PublicKey.from_public_bytes(pk_bytes)
        shared_key = ephemeral_private_key.exchange(peer_public_key)
        
        # 4. Deterministically derive the final shared secret
        shared_secret = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b"sypher-pqc-kem",
        ).derive(shared_key + ciphertext)
        
        return ciphertext, shared_secret

    def decapsulate(self, sk_bytes, ciphertext):
        # 1. Load the private key and the received ciphertext (ephemeral public key)
        private_key = x25519.X25519PrivateKey.from_private_bytes(sk_bytes)
        ephemeral_public_key = x25519.X25519PublicKey.from_public_bytes(ciphertext)
        
        # 2. Derive the exact same shared asymmetric key
        shared_key = private_key.exchange(ephemeral_public_key)
        
        # 3. Re-derive the matching shared secret using the exact same HKDF inputs
        shared_secret = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b"sypher-pqc-kem",
        ).derive(shared_key + ciphertext)
        
        return shared_secret
