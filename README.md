# SYPHER: Post-Quantum Cryptographic Intelligence & Routing Engine

[![Sypher Security Integrity Audit](https://github.com/barianlou/sypher/actions/workflows/sypher_security_audit.yml/badge.svg)](https://github.com/barianlou/sypher/actions)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![Java](https://img.shields.io/badge/Java-17%20LTS-orange.svg)
![C++](https://img.shields.io/badge/C%2B%2B-20-darkblue.svg)

**Architect:** Bijan Arianlou  
**Role:** Principal Systems Architect  
**Status:** Reference Implementation (v1.1)  
**Core Logic:** Hybrid Key Encapsulation (KEM) + Deep Q-Network (DQN) Routing

---

## 1. Architectural Intent

Sypher is a modular, reinforcement-driven cryptographic framework engineered to secure data transport against future quantum-decryption threats (“Store Now, Decrypt Later”). Unlike static cryptographic libraries, Sypher incorporates an autonomic **Deep Q-Network (DQN)** that continuously optimizes cryptographic routing under adversarial conditions such as DDoS floods, quantum-harvesting telemetry, and high-variance network volatility.

The system implements a hybrid protocol combining:

- **ML-KEM / Kyber-768** profile for post-quantum key encapsulation  
- **AES-256-GCM** for authenticated payload transport  
- **HKDF-SHA256** for deterministic secret expansion  

All governed by the **Hybrid_PQC_Evaluation** invariant:

$$\text{Viability\_Score} = (w_1 \cdot \text{Security\_Level}) - (w_2 \cdot \text{Latency\_Overhead}) - (w_3 \cdot \text{Size\_Overhead})$$

---

## 2. Language & System Integration (Triune Stack)

### Python 3.10 — Autonomic ML Core
- **TensorFlow / Keras:** Deep Q-Network policy backbone with Huber-loss gradient damping.
- **Gymnasium:** Continuous-state Markov Decision Process (MDP) adversarial threat simulation.
- **Cryptography Hazmat:** Montgomery Curve25519 (X25519), HKDF-SHA256, and AES-256-GCM primitives.
- Enforces Bellman updates, vector experience replays, and state-space variance clamping.

### Java 17 — Enterprise Integration Gateway
- **Spring Boot:** High-throughput, non-blocking asynchronous REST/Kafka ingestion layer.
- **Reactive Concurrency:** `CompletableFuture` pipelines isolate servlet worker threads from ML inference.
- **Perimeter Gate:** Enforces strict 28-byte minimum envelope boundaries (`12B Nonce + 16B Tag`) and session AAD integrity.

### C++20 — Native Hardware Guard
- **Zero-Allocation Cache Residency:** Statically sized circular buffers aligned to 64-byte boundaries (`alignas(64)`) to eliminate false sharing.
- **Microarchitectural Execution:** Lock-free atomic operations (`std::memory_order_relaxed` / `release`) enforce the **Structural_Veto_Gate** and **Bayesian_Dampener** in CPU L1/L2 cache.
- **Deterministic O(1) Velocity:** Nanosecond-level boundary checks drop anomalous actions before network dispatch.

---

## 3. Protocol Sequence (The Handshake)

Sypher establishes secure channels using an authenticated **Key Encapsulation Mechanism (KEM)** rather than vulnerable static RSA/ECC key exchanges. The DQN policy engine continuously samples threat telemetry to rotate parameters and select encapsulation schemes.

```text
  [ CLIENT / INGRESS ]                                  [ SYPHER ENGINE ]
           |                                                    |
           | 1. Ingress Request + Session ID                    |
           |--------------------------------------------------->|
           |                                                    | 2. Generate Static Pair
           |                                                    |    (s_r, P_r) via X25519
           | 3. Transmit Static Public Key (P_r)                |
           |<---------------------------------------------------|
           |                                                    |
           | 4. Sample Ephemeral Pair (s_e, P_e)                |
           |    Compute Secret: K = s_e * P_r                   |
           |    Derive Symmetric Key:                           |
           |      Key = HKDF-SHA256(K || P_e)                   |
           |    Encrypt Payload with AES-256-GCM                |
           |    AAD Binding: X-Session-ID                       |
           |                                                    |
           | 5. Dispatch Wire Payload (>= 28 Bytes)             |
           |    [ 12B Nonce || P_e || Ciphertext || 16B Tag ]   |
           |--------------------------------------------------->|
           |                                                    | 6. Spring Boot Edge Gate
           |                                                    |    Verify Envelope >= 28B
           |                                                    |    Check AAD Header Match
           |                                                    |
           |                                                    | 7. C++20 Hardware Guard
           |                                                    |    Validate Variance <= Cap
           |                                                    |    Execute O(1) Veto Gate
           |                                                    |
           |                                                    | 8. Decapsulate Shared Secret
           |                                                    |    Compute Secret: K = s_r * P_e
           |                                                    |    Derive Key via HKDF
           |                                                    |    Verify Galois GHASH Tag
           |                                                    |    Commit Plaintext State
           |                                                    |
           | 9. Cryptographic Acknowledgment                    |
           |<---------------------------------------------------|
