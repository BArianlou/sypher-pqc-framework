# SYPHER: Post-Quantum Cryptographic Intelligence & Dynamic Routing Engine

[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![C++20](https://img.shields.io/badge/C%2B%2B-20%20Standard-blue.svg)](https://en.cppreference.com/w/cpp/20)
[![Java 17](https://img.shields.io/badge/Java-17%20LTS-orange.svg)](https://aws.amazon.com/corretto/)
[![Post--Quantum](https://img.shields.io/badge/PQC-NIST%20FIPS%20203%20(ML--KEM)-green.svg)](https://csrc.nist.gov/pubs/fips/203/final)
[![Kafka](https://img.shields.io/badge/Apache%20Kafka-Distributed%20Ingestion-black.svg)](https://kafka.apache.org/)

**Architect:** Bijan Arianlou, MSEE  
**Role:** Principal Solutions & Systems Architect  
**Status:** Production Reference Architecture (v1.1)  
**Core Logic:** Hybrid Post-Quantum Key Encapsulation (ML-KEM/Kyber) + Deep Q-Network (DQN) Routing  

---

## 1. Architectural Intent

**SYPHER** is a modular, reinforcement-driven cryptographic routing framework designed to secure distributed data transport against Harvest Now, Decrypt Later (HNDL) quantum threats. Instead of relying on static cipher negotiation, SYPHER uses an adaptive Deep Q-Network (DQN) policy to optimize cipher selection, encapsulation parameters, and routing behavior under changing network conditions such as packet variance, congestion, and distributed denial-of-service pressure.

The system implements a production hybrid cryptographic protocol:

* **ML-KEM / Kyber-768 (NIST FIPS 203):** Lattice-based post-quantum key encapsulation mechanism (KEM).
* **X25519 Hybridization:** Classical elliptic-curve Diffie-Hellman fallback providing dual-layer security guarantees.
* **AES-256-GCM:** Authenticated Encryption with Associated Data (AEAD) for payload confidentiality and tamper-evidence.
* **HKDF-SHA256:** Transcript-bound key derivation for secure symmetric key expansion.

### Cryptographic Viability Objective

The routing agent evaluates cryptographic and performance feasibility using a balanced scoring function:

$$\text{ViabilityScore}_t = (w_1 \cdot \text{SecurityMargin}_t) - (w_2 \cdot \text{LatencyOverhead}_t) - (w_3 \cdot \text{PayloadOverhead}_t)$$

Weights $w_1, w_2, w_3$ adjust dynamically based on congestion indicators and endpoint telemetry.

---

## 2. Multi-Runtime Architecture

SYPHER uses a polyglot execution topology to separate RL decision logic, enterprise integration, and low-latency safety controls:

* **Python 3.10 — Adaptive Reinforcement Learning Core:**  
  TensorFlow/Keras DQN policy model with Huber loss stabilization, experience replay, and Gymnasium-based simulation for dynamic cipher parameter selection.

* **Java 17 — Enterprise Integration Gateway:**  
  Spring Boot & Kafka stream consumers handling encrypted state vectors and telemetry metadata through non-blocking reactive pipelines (CompletableFuture).

* **C++20 — Low-Latency Native Hardware Guard:**  
  Zero-allocation, cache-line-aligned (64-byte) atomic ring buffers providing deterministic O(1) memory residency and real-time operational guardrails.

---

## 3. Protocol Handshake Sequence

SYPHER establishes authenticated, forward-secure sessions using an optimized hybrid KEM workflow:

1. **Ephemeral Key Generation:**  
   Generates ephemeral post-quantum (ML-KEM / Kyber-768) and classical (X25519) keypairs per session.

2. **Hybrid Encapsulation:**  
   Encapsulates the shared secret, producing ciphertext tokens and public material.

3. **HKDF-SHA256 Transcript Binding:**  
   Binds exchange parameters, nonces, and identities into a unified symmetric key.

4. **AEAD Encryption:**  
   Encrypts payloads using AES-256-GCM with unique IVs and authenticated metadata.

5. **Adaptive Policy Evaluation:**  
   The DQN agent monitors RTT, throughput, and drop rates to adjust encapsulation strategy or key refresh intervals.

---

## 4. Core Capabilities

* **Quantum Resistance:** ML-KEM (Kyber-768) lattice-based key encapsulation aligned with modern PQC migration standards.
* **Forward Secrecy:** Ephemeral session keys with transcript-bound derivation.
* **Adaptive Routing Decisions:** DQN policy adjusts cipher selection based on real-time network conditions.
* **Replay Protection & Nonce Hygiene:** AES-256-GCM prevents replay attacks through authenticated headers.
* **Hardware-Level Guardrails:** C++20 atomic modules enforce deterministic safety thresholds at L1/L2 cache speeds.

---

## 5. Repository Architecture

```text
```text
sypher-pqc-engine/
├── .github/
│   └── workflows/
│       ├── polyglot_ci.yml         # Dual-runtime validation (Python, Java, C++20)
│       └── security_audit.yml      # Static analysis, memory sanitizers, and linters
├── src/
│   ├── ml_engine/                  # Python DQN policy graphs and Gymnasium MDP
│   ├── java_gateway/               # Spring Boot Kafka ingestion and REST interfaces
│   └── native_cpp/                 # C++20 lock-free ring buffers and circuit breakers
├── tests/
│   ├── test_kem_handshake.py       # PQC encapsulation and cryptographic validation
│   └── test_cpp_ring_buffer.cpp    # Concurrency and cache-alignment unit checks
├── Dockerfile                      # Multi-stage polyglot container build
├── requirements.txt                # Pinned Python dependencies
└── README.md                       # Architectural specification and documentation
```

## 6. Implementation & Compliance Notice
This repository contains the Reference Architecture, multi-runtime integration wrappers, and simulation environments. Production deployment requires:

formal cryptographic boundary audits

validated Hardware Security Module (HSM) key roots

organization-specific governance compliance

For enterprise integration manifests, native C++ bindings, or distributed deployment specifications:
Architect: Bijan Arianlou, MSEE
Role: Principal Solutions & Systems Architect

