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

> **Viability_Score** = (w₁ · Security_Level) − (w₂ · Latency_Overhead) − (w₃ · Size_Overhead)

---

## 2. Language & System Integration (Triune Stack)

### Python 3.10 — Autonomic ML Core

- TensorFlow (DQN policy backbone)  
- Gymnasium (MDP simulation)  
- Cryptography (AES-GCM, HKDF, X25519/Kyber primitives)  
- Implements adversarial training, Bellman updates, and state-space clamping.

### Java 17 — Enterprise Integration Gateway

- Spring Boot asynchronous REST/Kafka ingestion  
- Non-blocking `CompletableFuture` pipelines  
- High-throughput ingestion of encrypted state vectors  
- Enforces geometric payload boundaries (28-byte minimum envelope) and session-context fidelity.

### C++20 — Native Hardware Guard

- Zero-allocation, cache-aligned (64-byte) atomic ring buffers  
- Enforces **Structural_Veto_Gate** and **Bayesian_Dampener** at L1/L2 cache speed  
- Deterministic O(1) memory residency  
- Hardware-level veto against variance spikes and non-finite tensor outputs.

---

## 3. Protocol Sequence (The Handshake)

Sypher establishes secure channels using a **Key Encapsulation Mechanism (KEM)** rather than RSA/ECC. The RL agent continuously evaluates threat telemetry and latency to select optimal encapsulation strategies.

**Flow:**

1. Ephemeral PQC / X25519 keypair generation  
2. Kyber-768 baseline encapsulation  
3. HKDF-SHA256 expansion with transcript binding  
4. AES-256-GCM authenticated encryption (28-byte minimum envelope)  
5. RL-driven routing and scheme rotation
---

## 4. Core Capabilities

- **Quantum Resistance:** Kyber-768 lattice-based KEM profile with optional X25519 hybridization.  
- **Forward Secrecy:** Ephemeral secrets + deterministic HKDF expansion.  
- **Autonomic Adversarial Defense:** DQN-driven scheme rotation, Huber-loss stabilization, and state-space clamping.  
- **Absolute Data Supremacy:** AES-256-GCM AEAD binds payloads to session-specific AAD, neutralizing replay vectors.  
- **Deterministic Hardware Guardrails:** C++20 atomic ring buffers enforce nanosecond-level veto decisions.

---

## 5. Implementation Notice

This repository is a **Reference Architecture**.  
Direct use of raw cryptographic primitives in production environments requires formal review.

For enterprise integration, native C++ bindings, or deployment documentation:  
**Contact the Architect.**

---

## 6. Repository Structure (Triune Layout)
/ml-engine              # Python DQN + PQC cryptographic core
/java-gateway           # Spring Boot REST/Kafka ingestion layer
/native_cpp             # C++20 hardware guard (zero-allocation, lock-free)
/tests                  # Deterministic SCIENTIFIC_VALIDATION suite
Dockerfile              # Polyglot container architecture
requirements.txt        # Deterministic dependency graph
