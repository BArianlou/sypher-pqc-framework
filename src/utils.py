"""
===============================================================================
MODULE MANIFEST: SYPHER PAYLOAD ENCAPSULATION & SERIALIZATION
===============================================================================
System Purpose:
    Serves as the deterministic data-binding layer for the SYPHER engine.
    Bridges high-level autonomic agent states (dictionaries, metrics, commands)
    with the low-level symmetric authenticated encryption core (AES-256-GCM),
    guaranteeing tamper-proof, replay-resistant data transmission across
    untrusted adversarial networks.

State Boundaries:
    - Encapsulates canonical serialization, deserialization, and Associated
      Authenticated Data (AAD) session mapping.
    - Decoupled from Galois field polynomial evaluation, nonce generation,
      and low-level cipher state management delegated to SypherCipher.

Mathematical/Physical Invariants:
    1. Deterministic Canonical Serialization:
       Serialization enforces strict key ordering and compact whitespace stripping:
       JSON_Canonical(s) = dumps(s, sort_keys=True, separators=(',', ':'))
       guaranteeing bit-for-bit reproducible byte representations across disparate runtimes.
    2. Cryptographic Session Binding (AAD Replay Protection):
       Session tokens are bound as Associated Data into the Galois GHASH tag,
       mathematically invalidating replay attempts across differing network sessions.
    3. Payload Envelope Geometry:
       |Wire_Payload| = 12 (Nonce) + |Serialized_Plaintext| + 16 (Auth Tag).

Design Rationale:
    Uncontrolled serialization formats (e.g., platform-dependent whitespace or
    arbitrary key ordering) produce non-identical byte streams for equivalent
    state maps. This module enforces canonical serialization, upholding the Triune
    SESSION_CONTEXT_FIDELITY directive and preventing authentication tag mismatches.
===============================================================================
"""

import json
from typing import Any, Dict, Optional

# [STRUCTURAL CALLOUT] CI/CD Path Resolution & Isolation
# Guarantees robust module discovery whether imported as a package namespace
# or executed as an isolated unit test in containerized runner environments.
try:
    from .symmetric_cipher import SypherCipher
except ImportError:
    from symmetric_cipher import SypherCipher


def package_sypher_payload(
    agent_state: Dict[str, Any],
    shared_secret: bytes,
    session_id: Optional[bytes] = None,
) -> bytes:
    """Serializes and seals an agent state dictionary using AES-256-GCM.

    Encodes the state payload into a canonical JSON byte string and encrypts it,
    binding optional session identifiers into the AEAD authentication tag.

    Mathematical Invariants:
        - Deterministic Key Ordering: sort_keys=True enforces canonical key sequences.
        - Space Elimination: separators=(',', ':') removes variable whitespace tokens.
        - Envelope Length: |Ciphertext| = |Plaintext| + 28 bytes (12 Nonce + 16 Tag).

    Args:
        agent_state: Unencrypted state dictionary or command structure.
        shared_secret: 32-byte (256-bit) validated symmetric key.
        session_id: Optional ephemeral session identifier cryptographically
            bound to the authentication tag as Associated Authenticated Data (AAD).

    Returns:
        bytes: Encrypted byte buffer containing [12-byte Nonce || Ciphertext || 16-byte Tag].

    Raises:
        ValueError: If shared_secret does not conform to the 32-byte key boundary.
        TypeError: If agent_state contains non-JSON-serializable objects.
    """
    cipher: SypherCipher = SypherCipher(shared_secret)

    # [STRUCTURAL CALLOUT] Deterministic Serialization Lock
    # Canonical serialization: strips whitespace and forces lexicographical key sorting,
    # eliminating formatting divergence across platforms and minimizing packet size overhead.
    data_string: str = json.dumps(
        agent_state,
        sort_keys=True,
        separators=(",", ":"),
    )

    # [STRUCTURAL CALLOUT] Cryptographic Session Binding (AAD)
    # Binds session_id to the Galois authentication tag. Replaying this payload in
    # an alternate session context causes immediate tag failure during decryption.
    return cipher.encrypt(data_string, associated_data=session_id)


def unpack_sypher_payload(
    payload: bytes,
    shared_secret: bytes,
    session_id: Optional[bytes] = None,
) -> Dict[str, Any]:
    """Verifies AEAD authenticity, decrypts wire data, and parses the JSON state.

    Decrypts the payload using the provided key, validating that the ciphertext,
    nonce, and session AAD match the expected integrity tag before deserializing.

    Mathematical Invariants:
        - Cryptographic Veto: Tag verification failure aborts execution prior
          to payload deserialization.
        - State Recovery: Unpack(Package(s, k, sid), k, sid) == s for all valid state maps.

    Args:
        payload: Wire byte sequence containing [12-byte Nonce || Ciphertext || 16-byte Tag].
        shared_secret: 32-byte (256-bit) validated symmetric key.
        session_id: Optional session identifier matching the AAD used during encryption.

    Returns:
        Dict[str, Any]: Reconstructed agent state dictionary.

    Raises:
        ValueError: If payload length is < 28 bytes, or if AEAD tag validation fails
            due to tampering, payload corruption, or mismatched session context.
        json.JSONDecodeError: If decrypted plaintext fails JSON syntax parsing.
    """
    cipher: SypherCipher = SypherCipher(shared_secret)

    # [STRUCTURAL CALLOUT] Absolute Integrity Verification
    # Acts as a deterministic gate: decrypt() enforces GHASH tag verification.
    # Corrupted bytes or mismatched session IDs trigger an immediate ValueError.
    decrypted_data: str = cipher.decrypt(payload, associated_data=session_id)

    return json.loads(decrypted_data)
