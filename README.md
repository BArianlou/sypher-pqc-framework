# SYPHER: Post-Quantum Cryptographic Intelligence & Routing Engine

[![Sypher Security Integrity Audit](https://github.com/barianlou/sypher/actions/workflows/sypher_security_audit.yml/badge.svg)](https://github.com/barianlou/sypher/actions)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![Java](https://img.shields.io/badge/Java-17%20LTS-orange.svg)
![C++](https://img.shields.io/badge/C%2B%2B-20-darkblue.svg)

**Architect:** Bijan Arianlou | **Role:** Principal Systems Architect  
**Status:** Reference Implementation (v1.1) | **Core Logic:** Hybrid Key Encapsulation (KEM) + Adversarial DQN Routing

---

### 1. Architectural Intent
Sypher is a modular, autonomic cryptographic execution engine engineered to defend enterprise data transport against harvest-now, decrypt-later quantum threats. Moving beyond static cipher configurations, Sypher integrates an adaptive **Deep Q-Network (DQN)** policy engine that dynamically optimizes cryptographic parameters and key-rotation intervals under non-stationary adversarial conditions (e.g., volumetric floods, latency degradation, targeted key extraction).

The framework implements a Hybrid Protocol architecture, evaluating NIST-standardized Post-Quantum algorithms (ML-KEM / Kyber-768 profile) alongside hardened classical primitives (X25519) for key encapsulation, paired with authenticated symmetric stream encryption (AES-256-GCM). Defensive routing decisions continuously maximize the objective function defined by the `Hybrid_PQC_Evaluation` mathematical invariant:

$$\text{Viability\_Score} = (w_1 \cdot \text{Security\_Level}) - (w_2 \cdot \text{Latency\_Overhead}) - (w_3 \cdot \text{Size\_Overhead})$$

---

### 2. Polyglot Architecture (The Triune Stack)
* **Core Autonomic Engine (Python 3.10):** TensorFlow/Keras, Gymnasium, and Cryptography hazmat primitives. Executes the adversarial Markov Decision Process (MDP), experience replay batch vectorization, and Huber-loss regularized gradient backpropagation.
* **Enterprise Integration Gateway (Java 17 / Spring Boot):** Asynchronous, non-blocking REST/Kafka ingress microservices. Enforces a 28-byte edge envelope validation gate (`12-byte Nonce + 16-byte GHASH Tag`) and delegates execution via `CompletableFuture` to preserve JVM thread-pool capacity.
* **Native Hardware Guard (C++20):** Lock-free, zero-allocation memory safety controller. Pinpoints cache lines to 64-byte boundaries (`alignas(64)`) to eliminate false sharing, enforcing the `Structural_Veto_Gate` and `Bayesian_Dampener` bounds directly in CPU cache with O(1) time complexity.

---

### 3. Protocol Sequence (The Handshake)
The system executes a ciphertext-bound Key Encapsulation Mechanism (KEM) to derive ephemeral 256-bit symmetric shared secrets over untrusted channels:
