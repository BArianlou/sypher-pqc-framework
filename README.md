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

All governed by the **Hybrid_PQC_Evaluation** invariant.

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

```mermaid
sequenceDiagram
    autonumber
    actor Client as Client / Ingress
    participant Gateway as Java 17 Gateway<br/>(Spring Boot REST)
    participant Guard as C++20 Native Guard<br/>(Lock-Free Cache Gate)
    participant Core as Python 3.10 Core<br/>(DQN + PQC Engine)

    Note over Client: Encapsulate KEM Payload<br/>[12B Nonce || P_e (32B) || Ciphertext || 16B GHASH Tag]
    Client->>+Gateway: POST /api/v1/sypher/secure-inference<br/>Header: X-Session-ID (AAD)

    rect rgb(24, 28, 36)
        Note over Gateway: Edge Geometric Veto<br/>Assert: len(Payload) >= 28 Bytes<br/>Assert: X-Session-ID Present & Non-Blank
        Gateway->>+Guard: validate_and_clamp_action()<br/>Pass Telemetry + Variance
        
        Note over Guard: O(1) Atomic Hardware Gate<br/>Check: isfinite(action_value)<br/>Clamp: variance <= max_variance_bound_<br/>Commit Slot (std::memory_order_release)
        
        alt Structural Veto Triggered
            Guard-->>Gateway: false (VETO: transition_prob = 0.0)
            Gateway-->>Client: 400 Bad Request / 500 Clamped
        else Boundary Cleared
            Guard-->>-Gateway: true (PROCEED)
            Gateway->>+Core: CompletableFuture Dispatch (Async IPC / gRPC)
            
            Note over Core: 1. Decapsulate Kyber-768 / X25519 Secret<br/>2. Derive Session Key via HKDF-SHA256<br/>3. Verify Galois GHASH Tag with AAD<br/>4. DQN Step: State Evaluation & Reward
            Core-->>-Gateway: Decrypted State + Routing Decision
        end
    end

    Gateway-->>-Client: 200 OK (Cryptographic Ack)

[ CLIENT / INGRESS ]
          |
          |  POST /api/v1/sypher/secure-inference
          |  Headers: [ X-Session-ID: <AAD_UUID> ]
          |  Payload: [ 12B Nonce || P_e (32B) || Ciphertext || 16B Tag ]
          v
+-------------------------------------------------------------------------------+
| SYPHER TRIUNE ARCHITECTURE                                                    |
|                                                                               |
|  [ LAYER 1: JAVA 17 ENTERPRISE GATEWAY ]                                      |
|    |-- Spring Boot Non-Blocking Async Ingestion (CompletableFuture)           |
|    |-- Perimeter Check: Validate Payload >= 28 Bytes                          |
|    `-- Header Check: Validate Session AAD Context                             |
|          |                                                                    |
|          | (Telemetry: Action ID, Q-Value, State Variance)                    |
|          v                                                                    |
|  [ LAYER 2: C++20 NATIVE HARDWARE GUARD ]                                     |
|    |-- Microarchitectural Lock-Free Core (alignas(64) Ring Buffer)            |
|    |-- Check: isfinite(action_value)                                          |
|    `-- Bayesian Dampener: Check state_variance <= max_variance_bound_         |
|          |                                                                    |
|          +---> [FAIL] --> STRUCTURAL VETO (transition_prob = 0.0)             |
|          |                                                                    |
|          +---> [PASS] --> Commit Slot via std::memory_order_release           |
|          |                                                                    |
|          v                                                                    |
|  [ LAYER 3: PYTHON 3.10 AUTONOMIC ML CORE ]                                   |
|    |-- Decapsulate Shared Secret K = s_r * P_e (Kyber-768 / X25519)           |
|    |-- Derive Symmetric Key = HKDF-SHA256(K || P_e)                          |
|    |-- Verify Galois GHASH Tag (Session AAD Binding)                          |
|    `-- Adversarial DQN Policy Step (Huber Loss Gradient Clamping)             |
+-------------------------------------------------------------------------------+
          |
          |  200 OK (Execution Validated)
          v
 [ CLIENT / INGRESS ]
