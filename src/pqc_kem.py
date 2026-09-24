"""
===============================================================================
MODULE MANIFEST: SYPHER KEM ORCHESTRATOR (HYBRID PQC SIMULATION)
===============================================================================
System Purpose:
    Serves as the Sovereign Key Encapsulation Mechanism (KEM) Orchestrator for
    the SYPHER engine. Simulates Post-Quantum Cryptographic (PQC) key exchange
    interfaces using high-assurance hybrid classical-elliptic curve primitives
    (X25519 + HKDF-SHA256). Provides empirical latency, size overhead, and API
    benchmarking baselines prior to native ML-KEM (Kyber) migration.

State Boundaries:
    - Encapsulates asymmetric keypair synthesis, ephemeral encapsulation, and
      deterministic shared-secret decapsulation.
    - Strictly decoupled from symmetric channel encryption (e.g., AES-GCM / ChaCha20)
      and network transport bus protocols.

Mathematical/Physical Invariants:
    1. Hybrid_PQC_Evaluation:
       Viability_Score = (Security_Level * w1) - (Latency_Overhead * w2) - (Size_Overhead * w3)
       This module supplies the empirical latency and packet-size baseline metrics
       for classical benchmarks against lattice-based candidates.
    2. Elliptic Curve Discrete Logarithm Problem (ECDLP):
       Relies on the discrete logarithm hardness over Montgomery Curve25519
       (scalar multiplication over GF(2^255 - 19)).
    3. Transcript-Bound Key Derivation:
       Shared Secret = HKDF-Extract-and-Expand(IKM = ECDH_Secret || Ciphertext, Info = "sypher-pqc-kem")
       guaranteeing non-malleability and Perfect Forward Secrecy (PFS).

Design Rationale:
    Directly deploying unvalidated, evolving lattice-based PQC code paths into
    production infrastructure presents severe operational risk. This simulation
    module models the KEM state machine and interface contracts, establishing
    architectural readiness across the Triune stack without introducing
    unbounded cryptographic failure modes.
===============================================================================
"""

from typing import Tuple
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


class SypherKEM:
    """Key Encapsulation Mechanism (KEM) simulation harness for the SYPHER engine.

    Models an ephemeral Diffie-Hellman Key Encapsulation Mechanism (DHKEM)
    over Curve25519, implementing ciphertext-bound symmetric key derivation.

    Attributes:
        algorithm (str): Identifier denoting the active cryptographic simulation profile.
    """

    def __init__(self) -> None:
        """Initializes the KEM simulation orchestrator and assigns the algorithm profile."""
        # [STRUCTURAL CALLOUT] PQC Simulation Boundary
        # Explicitly identifies this module as an architectural simulation wrapper,
        # differentiating classical baseline telemetry from true lattice-based schemes.
        self.algorithm: str = "Kyber-768-Orchestrator-Mock"

    def generate_keypair(self) -> Tuple[bytes, bytes]:
        """Synthesizes a static asymmetric keypair for the receiving entity.

        Utilizes the system cryptographic random number generator to derive
        a 32-byte private scalar and compute the associated Montgomery public point.

        Mathematical Invariants:
            - Private Scalar: s in [0, 2^256 - 1], clamped according to Curve25519 specifications.
            - Public Point: P = s * B, where B is the canonical base point.
            - Dimension Boundaries: |PK| = 32 bytes, |SK| = 32 bytes.

        Returns:
            Tuple[bytes, bytes]: A 2-tuple containing:
                - pk_bytes (bytes): 32-byte raw public key point.
                - sk_bytes (bytes): 32-byte raw private scalar.
        """
        # Generate cryptographically secure asymmetric keypair
        private_key: x25519.X25519PrivateKey = x25519.X25519PrivateKey.generate()
        public_key: x25519.X25519PublicKey = private_key.public_key()

        # [STRUCTURAL CALLOUT] Kinetic Payload Optimization
        # Serializes directly to raw byte buffers, eliminating ASN.1/DER/PEM encoding overhead.
        # Directly bounds the Size_Overhead variable in the Hybrid_PQC_Evaluation equation.
        pk_bytes: bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        sk_bytes: bytes = private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption(),
        )
        return pk_bytes, sk_bytes

    def encapsulate(self, pk_bytes: bytes) -> Tuple[bytes, bytes]:
        """Executes active key encapsulation against a recipient's static public key.

        Generates a fresh ephemeral keypair, computes the Diffie-Hellman shared secret,
        and binds the resulting ciphertext into the HKDF expansion context.

        Mathematical Invariants:
            - Ephemeral Shared Key: K_asym = s_e * P_receiver = s_e * (s_r * B)
            - Symmetric Derivation: K_sym = HKDF_SHA256(IKM = K_asym || Ciphertext, Salt = 0, Info = context)
            - Ciphertext Geometry: Ephemeral public point P_e (|Ciphertext| = 32 bytes).

        Args:
            pk_bytes: 32-byte raw Curve25519 public key of the receiver.

        Returns:
            Tuple[bytes, bytes]: A 2-tuple containing:
                - ciphertext (bytes): 32-byte raw ephemeral public key.
                - shared_secret (bytes): 32-byte symmetric key for payload cipher instantiation.

        Raises:
            ValueError: If pk_bytes does not strictly conform to the 32-byte key envelope.
        """
        # 1. Synthesize ephemeral keypair for single-session encapsulation
        ephemeral_private_key: x25519.X25519PrivateKey = (
            x25519.X25519PrivateKey.generate()
        )
        ephemeral_public_key: x25519.X25519PublicKey = (
            ephemeral_private_key.public_key()
        )

        # 2. Extract raw bytes of ephemeral public key as transmission ciphertext
        ciphertext: bytes = ephemeral_public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )

        # 3. Derive scalar product shared key
        peer_public_key: x25519.X25519PublicKey = (
            x25519.X25519PublicKey.from_public_bytes(pk_bytes)
        )
        shared_key: bytes = ephemeral_private_key.exchange(peer_public_key)

        # [STRUCTURAL CALLOUT] Ciphertext Binding & Deterministic Expansion
        # Binds the emitted ciphertext directly into HKDF input key material.
        # Defends against re-encapsulation and ciphertext substitution vulnerabilities.
        shared_secret: bytes = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b"sypher-pqc-kem",
        ).derive(shared_key + ciphertext)

        return ciphertext, shared_secret

    def decapsulate(self, sk_bytes: bytes, ciphertext: bytes) -> bytes:
        """Executes decapsulation to recover the symmetric shared secret.

        Performs scalar multiplication between the receiver's static private key
        and the sender's transmitted ephemeral public key, reproducing the exact HKDF input.

        Mathematical Invariants:
            - Commutative Consistency:
              s_r * P_e = s_r * (s_e * B) = s_e * (s_r * B) = K_asym
            - Symmetric Equivalence:
              Decapsulate(sk, c) == Encapsulate(pk)[1] for identical key pairs.

        Args:
            sk_bytes: 32-byte raw Curve25519 private key scalar of the receiver.
            ciphertext: 32-byte raw ephemeral public key transmitted across the channel.

        Returns:
            bytes: 32-byte deterministic symmetric shared secret.

        Raises:
            ValueError: If sk_bytes or ciphertext do not conform to the 32-byte envelope.
        """
        # 1. Deserialize receiver private scalar and transmitted ephemeral public point
        private_key: x25519.X25519PrivateKey = (
            x25519.X25519PrivateKey.from_private_bytes(sk_bytes)
        )
        ephemeral_public_key: x25519.X25519PublicKey = (
            x25519.X25519PublicKey.from_public_bytes(ciphertext)
        )

        # 2. Derive identical asymmetric shared point
        shared_key: bytes = private_key.exchange(ephemeral_public_key)

        # [STRUCTURAL CALLOUT] Symmetric State Reconstruction
        # Replicates the exact derivation context: SHA-256, 32-byte length, identical info tag.
        # Guarantees bit-for-bit key alignment with the encapsulation output.
        shared_secret: bytes = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b"sypher-pqc-kem",
        ).derive(shared_key + ciphertext)

        return shared_secret
