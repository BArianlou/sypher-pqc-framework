[![Sypher Security Integrity Audit](https://github.com/BArianlou/sypher-pqc-framework/actions/workflows/integrity_audit.yml/badge.svg)](https://github.com/BArianlou/sypher-pqc-framework/actions/workflows/integrity_audit.yml)
![Security](https://img.shields.io/badge/Security-Post--Quantum-blueviolet)
![Algorithm](https://img.shields.io/badge/Algorithm-Kyber--1024%20%2B%20AES--256-blue)
![License](https://img.shields.io/badge/license-PROPRIETARY-red?style=flat-square)

**Architect:** Bijan Arianlou | **Role:** Principal Systems Architect
**Status:** Reference Implementation (v1.1) | **Core Logic:** Hybrid Key Encapsulation (KEM)

---

## 1. Architectural Intent
Sypher is a modular cryptographic framework designed to secure data transport against future quantum-decryption threats ("Store Now, Decrypt Later"). It implements a **Hybrid Protocol**, combining NIST-standardized Post-Quantum algorithms (Kyber) for key encapsulation with battle-tested symmetric encryption (AES-256-GCM) for payload transport.

## 2. Protocol Sequence (The Handshake)
The system utilizes a "Key Encapsulation Mechanism" (KEM) to establish a shared secret over an insecure channel, bypassing the vulnerabilities of RSA/ECC.

### Cryptographic Flow (Live Render)
```mermaid
sequenceDiagram
    participant Alice as Client (Initiator)
    participant Bob as Server (Listener)
    
    Note over Alice, Bob: Phase 1: Post-Quantum Key Exchange (Kyber)
    Bob->>Alice: Public Key (pk) [Kyber-1024]
    Alice->>Alice: Generate Random Seed
    Alice->>Alice: Encapsulate Seed -> Shared Secret (SS) + Ciphertext (c)
    Alice->>Bob: Transmit Ciphertext (c)
    Bob->>Bob: Decapsulate (c) with Secret Key (sk) -> Shared Secret (SS)
    
    Note over Alice, Bob: Phase 2: Symmetric Tunnel (AES-256-GCM)
    Alice->>Alice: Encrypt Payload with SS (AES-GCM)
    Alice->>Bob: Transmit Encrypted Data + Auth Tag
    Bob->>Bob: Verify Tag & Decrypt with SS
    
    Note right of Bob: Secure Channel Established
```


### Core Capabilities
*   **Quantum Resistance:** Utilizes Kyber-1024 (NIST PQC Winner).
*   **Forward Secrecy:** Ephemeral key generation.
*   **Hybrid Architecture:** Merges AES speed with Lattice security.

---

## Implementation Notice
This repository serves as a **Reference Architecture**.
> *Contact the Architect for integration documentation.*
