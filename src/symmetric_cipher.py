```python
"""
===============================================================================
MODULE MANIFEST: SYPHER SYMMETRIC EXECUTION CORE (AES-256-GCM)
===============================================================================
System Purpose:
    Serves as the deterministic symmetric encryption layer for the SYPHER
    engine. Executes Authenticated Encryption with Associated Data (AEAD)
    using AES-256-GCM to guarantee both confidentiality and cryptographic
    integrity of payloads post-encapsulation.

State Boundaries:
    - Strictly confined to symmetric state transformations and Galois field
      authentication over data-in-transit.
    - Delegates asymmetric key exchange and quantum-resistant key encapsulation
      to the SypherKEM orchestrator.

Mathematical/Physical Invariants:
    1. Galois/Counter Mode (GCM) Integrity:
       Enforces cryptographic binding between ciphertext, optional associated data,
       and the 128-bit authentication tag computed via GHASH over GF(2^128).
    2. Post-Quantum Symmetric Key Margin:
       Keys are clamped strictly to 256 bits (32 bytes). Under Grover's quantum
       search algorithm, effective complexity scales as O(2^(k/2)), preserving
       a minimum 128-bit security boundary against quantum cryptanalysis.
    3. Nonce Uniqueness Invariant:
       Every encryption call consumes a fresh, cryptographically secure 96-bit
       (12-byte) nonce. Nonce reuse with identical keys destroys Galois field
       authenticity and is strictly prevented.

Design Rationale:
    Unauthenticated encryption modes (e.g., CBC without HMAC) remain vulnerable
    to chosen-ciphertext attacks (CCA) and padding oracle exploits. AES-256-GCM
    provides hardware-accelerated kinetic efficiency via AES-NI and CLMUL instructions
    alongside native AEAD guarantees, enforcing the Triune DATA_SUPREMACY directive.
===============================================================================
"""

import os
from typing import Optional
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class SypherCipher:
    """Authenticated Encryption with Associated Data (AEAD) symmetric execution engine.

    Protects data-in-transit using AES-256-GCM with dynamic nonce injection
    and Galois field authentication tag verification.

    Attributes:
        key (bytes): 32-byte (256-bit) validated symmetric key.
        aesgcm (AESGCM): Instantiated Cryptography AEAD cipher engine.
    """

    def __init__(self, shared_secret: bytes) -> None:
        """Initializes the AES-256-GCM context and validates key geometry.

        Args:
            shared_secret: 32-byte symmetric key derived from post-quantum KEM
                or ephemeral Diffie-Hellman key exchange.

        Raises:
            ValueError: If shared_secret does not equal exactly 32 bytes (256 bits).
        """
        # [STRUCTURAL CALLOUT] Post-Quantum Key Space Enforcement
        # Grover's algorithm halves effective symmetric key length. Enforcing
        # a strict 32-byte key maintains a resilient 128-bit quantum security margin.
        if len(shared_secret) != 32:
            raise ValueError(
                f"SypherCipher requires a 256-bit (32-byte) shared secret; "
                f"received {len(shared_secret)} bytes."
            )
        self.key: bytes = shared_secret
        self.aesgcm: AESGCM = AESGCM(self.key)

    def encrypt(
        self, plaintext: str, associated_data: Optional[bytes] = None
    ) -> bytes:
        """Encrypts and authenticates a string payload using AES-GCM.

        Generates a 96-bit random nonce, encrypts the UTF-8 encoded plaintext,
        appends the 128-bit Galois authentication tag, and prepends the nonce
        for self-contained network transmission.

        Mathematical Invariants:
            - Nonce Length: Exactly 12 bytes (96 bits) drawn from OS CSPRNG.
            - Tag Length: Exactly 16 bytes (128 bits) computed over GF(2^128).
            - Output Geometry: |Output| = 12 (Nonce) + |Ciphertext| + 16 (Tag).

        Args:
            plaintext: UTF-8 string payload to be encrypted.
            associated_data: Optional unencrypted metadata cryptographically
                bound to the authentication tag without being ciphered.

        Returns:
            bytes: Byte sequence containing prepended nonce, ciphertext, and tag.
        """
        # [STRUCTURAL CALLOUT] Deterministic Nonce Geometry
        # AES-GCM requires a 96-bit nonce to prevent counter-wrap vulnerabilities
        # and optimize GHASH computation.
        nonce: bytes = os.urandom(12)

        # [STRUCTURAL CALLOUT] AAD Binding & State Transformation
        # Binds unencrypted metadata into the GHASH evaluation, ensuring routing
        # headers cannot be altered in-transit without invalidating the payload.
        ciphertext: bytes = self.aesgcm.encrypt(
            nonce, plaintext.encode("utf-8"), associated_data
        )

        # Prepend nonce for stateless transport
        return nonce + ciphertext

    def decrypt(
        self, encrypted_payload: bytes, associated_data: Optional[bytes] = None
    ) -> str:
        """Verifies authentication integrity and decrypts an AEAD payload.

        Extracts the prepended 12-byte nonce, verifies the 16-byte Galois
        authentication tag against the ciphertext and associated data, and
        decodes the decrypted bytes to UTF-8.

        Mathematical Invariants:
            - Minimum Geometry: |Payload| >= 28 bytes (12-byte Nonce + 16-byte Tag).
            - Galois Verification: Decryption succeeds if and only if ciphertext,
              nonce, and AAD match the encryption transcript exactly.

        Args:
            encrypted_payload: Byte sequence containing [12-byte Nonce || Ciphertext || 16-byte Tag].
            associated_data: Optional authenticated metadata matching the encryption input.

        Returns:
            str: Decrypted and authenticated UTF-8 plaintext string.

        Raises:
            ValueError: If payload length is below 28 bytes, or if authentication
                tag validation fails (tampering, corruption, or key mismatch).
            UnicodeDecodeError: If decrypted bytes fail UTF-8 string decoding.
        """
        # [STRUCTURAL CALLOUT] Defensive Tensor Slicing
        # Rejects payloads smaller than minimum envelope: 12-byte nonce + 16-byte tag.
        if len(encrypted_payload) < 28:
            raise ValueError(
                f"Payload too short ({len(encrypted_payload)} bytes). "
                "Minimum GCM envelope requires at least 28 bytes (12-byte nonce + 16-byte tag)."
            )

        nonce: bytes = encrypted_payload[:12]
        ciphertext_and_tag: bytes = encrypted_payload[12:]

        try:
            # [STRUCTURAL CALLOUT] Cryptographic Veto Gate
            # GHASH evaluation verifies the authentication tag. A single bit alteration
            # triggers InvalidTag, halting execution before malformed data is consumed.
            plaintext_bytes: bytes = self.aesgcm.decrypt(
                nonce, ciphertext_and_tag, associated_data
            )
            return plaintext_bytes.decode("utf-8")
        except InvalidTag as exc:
            # [STRUCTURAL CALLOUT] Absolute Integrity Enforcement
            # Translates cryptographic verification failure into a deterministic system veto.
            raise ValueError(
                "SYPHER INTEGRITY FATAL: Authentication tag verification failed. "
                "Payload modified, corrupted, or mismatched associated data."
            ) from exc
```
