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

Sypher is a modular, reinforcement-driven cryptographic execution framework engineered to secure data transport against harvest-now, decrypt-later quantum threats. Moving beyond static cipher baselines, Sypher incorporates an autonomic **Deep Q-Network (DQN)** that dynamically optimizes cryptographic parameters and scheme selection under non-stationary adversarial conditions, including volumetric DDoS floods, quantum-harvesting telemetry anomalies, and high-variance network volatility.

The system enforces a hybrid cryptographic protocol:
- **ML-KEM / Kyber-768** profile for lattice-based post-quantum key encapsulation
- **AES-256-GCM** for authenticated symmetric payload transport with Associated Authenticated Data (AAD)
- **HKDF-SHA256** for deterministic, transcript-bound secret expansion

Defensive routing decisions continuously maximize the objective function defined by the **Hybrid_PQC_Evaluation** invariant:

$$\text{Viability\_Score} = (w_1 \cdot \text{Security\_Level}) - (w_2 \cdot \text{Latency\_Overhead}) - (w_3 \cdot \text{Size\_Overhead})$$

---

## 2. Language & System Integration (Triune Stack)

### Python 3.10 — Autonomic ML Core
- **TensorFlow / Keras:** Deep Q-Network policy backbone stabilized via Huber-loss gradient damping ($\delta = 1.0$).
- **Gymnasium:** Continuous Markov Decision Process (MDP) adversarial threat simulation (`spaces.Box`, `spaces.Discrete`).
- **Cryptography Hazmat:** Montgomery Curve25519 (X25519), HKDF-SHA256, and AES-256-GCM primitives.
- Enforces Bellman value iteration, vectorized experience replay, and mathematical state-space clamping.

### Java 17 — Enterprise Integration Gateway
- **Spring Boot:** High-throughput, non-blocking asynchronous REST/Kafka ingestion layer.
- **Reactive Concurrency:** `CompletableFuture` pipelines isolate servlet worker threads from downstream inference loops.
- **Perimeter Gate:** Enforces the strict 28-byte minimum envelope invariant (`12B Nonce + 16B GHASH Tag`) and session AAD integrity.
- **Zero-GC Object Pooling:** `AtomicReferenceArray` of pre-allocated, mutable flyweight vectors to prevent Eden-space churn.

### C++20 — Native Hardware Guard
- **Zero-Allocation Cache Residency:** Statically sized 1024-slot circular buffer aligned to 64-byte boundaries (`alignas(64)`) to eliminate false sharing across CPU cores.
- **Microarchitectural Execution:** Lock-free atomic operations (`std::memory_order_relaxed` / `release`) enforce the **Structural_Veto_Gate** and **Bayesian_Dampener** directly in L1/L2 cache.
- **Deterministic O(1) Velocity:** Nanosecond-level boundary checks drop anomalous actions and non-finite tensor outputs ($\text{NaN} / \pm\infty$) before network dispatch.

---

## 3. Protocol Sequence (The Handshake)

Sypher establishes secure channels using an authenticated Key Encapsulation Mechanism (KEM) rather than static RSA/ECC key exchanges. The DQN policy engine continuously samples threat telemetry to rotate parameters and select encapsulation postures.

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
