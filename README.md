# ===============================================================================
# MODULE MANIFEST: SYPHER DETERMINISTIC DEPENDENCY GRAPH (REQUIREMENTS)
# ===============================================================================
# System Purpose:
#     Serves as the foundational mathematical and cryptographic registry for the
#     SYPHER engine. Defines the strict library envelopes required to instantiate
#     the adversarial Deep Q-Network, the post-quantum simulation primitives,
#     and the continuous Markov Decision Process (MDP) threat environment.
#
# State Boundaries:
#     - Strictly manages the Python execution environment and ABI boundaries.
#     - Prevents upstream package mutations and semantic version drift from
#       corrupting tensor geometries, gradient stability, or Galois field
#       authentication tags during CI/CD deployment phases.
#
# Mathematical/Physical Invariants:
#     1. SESSION_CONTEXT_FIDELITY:
#        Enforces reproducible computational baselines across local sandboxes,
#        ephemeral CI/CD runners, and containerized Kubernetes clusters.
#     2. Compatible Release Bounding (~= / <):
#        Enforces verified API feature floors while establishing upper-bound
#        ceilings against breaking major runtime mutations.
#
# Design Rationale:
#     Unpinned dependencies in deep reinforcement learning and cryptographic
#     pipelines introduce catastrophic non-determinism, C-ABI breakages, and
#     vulnerability exposure. This manifest acts as a structural lock, ensuring
#     that the neural backbones and AEAD ciphers compile identically across all
#     deployment targets.
# ===============================================================================

# [STRUCTURAL CALLOUT] Core Tensor Geometry & Vectorization
# Architectural Mandate: Provides foundational C-optimized ndarrays required
# for vectorized Bellman target updates and dimension-safe state reshaping in
# RLAgent. Clamped below 2.0.0 to prevent C-API breaking changes with compiled extensions.
numpy>=1.24.0,<2.0.0

# [STRUCTURAL CALLOUT] Adversarial Neural Topology & Gradient Control
# Instantiates the computational graph for the SypherAI backbone. Enforces
# numerical stability for Huber loss execution (Kinetic Gradient Control)
# during simulated network flash-floods and DDoS telemetry shocks.
tensorflow>=2.15.0,<2.17.0

# [STRUCTURAL CALLOUT] Adversarial MDP Simulation Boundaries
# Replaces deprecated gym APIs. Gymnasium 0.29.1+ provides spaces.Box and
# spaces.Discrete specifications that enforce deterministic observation and
# action boundaries within SypherSecurityEnv.
gymnasium>=0.29.1,<1.1.0

# [STRUCTURAL CALLOUT] Sovereign Cryptographic Primitives
# Foundational cryptographic engine. Clamped to versions containing hardened
# hazmat primitives for X25519 (Elliptic Curve KEM), HKDF (Deterministic
# Expansion), and AES-256-GCM (Galois/Counter Mode AEAD).
cryptography>=41.0.0,<44.0.0

# [STRUCTURAL CALLOUT] Telemetry Alignment & State-Space Fusion
# Supports local data transformation and tabular feature alignment. Guarantees
# deterministic handling of high-frequency telemetry via the Anti-Drift Truncation Lock.
pandas>=2.1.0,<3.0.0

# [STRUCTURAL CALLOUT] Automated Verification Gate
# Foundational harness for running deterministic pre-flight checks and unit
# assertions in CI/CD pipelines and containerized staging pods.
pytest>=7.4.0,<9.0.0
flake8>=6.1.0,<8.0.0
