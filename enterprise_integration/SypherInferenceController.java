/**
 * ===============================================================================
 * MODULE MANIFEST: SYPHER ENTERPRISE INTEGRATION GATEWAY (REST CONTROLLER)
 * ===============================================================================
 * System Purpose:
 *     Serves as the secure Enterprise Integration Gateway for the SYPHER engine
 *     (Logic Map Node 1: Ingestion & Validation). Bridges the untrusted external
 *     network boundary with internal Python-based cryptographic (AES-256-GCM/Kyber)
 *     and Deep Q-Network (DQN) policy inference engines.
 *
 * State Boundaries:
 *     - Strictly manages HTTP/REST network I/O, edge header extraction, wire payload
 *       geometry verification, and asynchronous thread delegation.
 *     - Decoupled from symmetric AEAD decryption, Galois polynomial evaluation,
 *       and neural policy optimization delegated to the Python execution tier.
 *
 * Mathematical/Physical Invariants:
 *     1. Geometric Payload Veto:
 *        Enforces the minimum AES-256-GCM envelope boundary at the network edge:
 *        |Payload| >= 28 bytes (12-byte Nonce + 16-byte Galois Authentication Tag)
 *        before allocating downstream RPC or serialization resources.
 *     2. Asynchronous Kinetic Flow:
 *        Non-blocking I/O via CompletableFuture ensures the JVM thread pool
 *        is not exhausted during computationally intensive neural inference.
 *
 * Design Rationale:
 *     Synchronous REST endpoints introduce thread starvation when coupled with
 *     deep learning inference backbones. This architecture utilizes non-blocking
 *     asynchronous pipelines to maintain high ingestion throughput, enforcing
 *     the Triune DATA_SUPREMACY directive to absorb high-velocity traffic without
 *     destabilizing the host JVM.
 * ===============================================================================
 */

package com.sypher.enterprise.api;

import java.util.Objects;
import java.util.concurrent.CompletableFuture;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * High-throughput asynchronous REST gateway for the SYPHER cryptographic routing engine.
 *
 * <p>Validates raw wire payload geometry, sanitizes transport headers, and delegates
 * encrypted execution requests to the underlying routing service.</p>
 */
// [STRUCTURAL CALLOUT] Spring IoC & Stateless Gateway
// Registers the controller as a stateless singleton within the Spring application context,
// guaranteeing thread-safe, non-blocking routing of adversarial state vectors.
@RestController
@RequestMapping("/api/v1/sypher")
public final class SypherInferenceController {

    private static final Logger logger = LoggerFactory.getLogger(SypherInferenceController.class);

    /**
     * Minimum permissible length for an AES-256-GCM wire envelope:
     * 12 bytes (96-bit Nonce) + 16 bytes (128-bit Galois Authentication Tag).
     */
    private static final int MINIMUM_GCM_ENVELOPE_BYTES = 28;

    private final SypherRoutingService routingService;

    /**
     * Constructs the gateway controller with the backing routing service.
     *
     * @param routingService Service responsible for cross-stack Python/gRPC dispatch;
     *                       must not be {@code null}.
     */
    public SypherInferenceController(final SypherRoutingService routingService) {
        this.routingService = Objects.requireNonNull(routingService, "routingService must not be null");
    }

    /**
     * Ingests, validates, and dispatches an encrypted inference payload asynchronously.
     *
     * <p>Performs edge geometric bounding on the payload buffer. Payloads failing the
     * 28-byte minimum threshold are rejected immediately with HTTP 400 Bad Request,
     * protecting internal compute resources from unviable operations.</p>
     *
     * @param sessionId Ephemeral session identifier passed via {@code X-Session-ID}
     *                  header, mapped directly to AES-GCM Associated Data (AAD).
     * @param encryptedPayload Raw byte buffer containing [Nonce || Ciphertext || Auth Tag].
     * @return A {@link CompletableFuture} wrapping the HTTP response entity.
     */
    @PostMapping(value = "/secure-inference", consumes = "application/octet-stream")
    public CompletableFuture<ResponseEntity<String>> processSecurePayload(
            @RequestHeader("X-Session-ID") final String sessionId,
            @RequestBody final byte[] encryptedPayload
    ) {
        // [STRUCTURAL CALLOUT] Context Boundary Guard
        // Rejects requests with missing or empty session headers prior to allocation.
        if (sessionId == null || sessionId.isBlank()) {
            logger.warn("GATEWAY VETO: Missing or blank X-Session-ID header.");
            return CompletableFuture.completedFuture(
                    ResponseEntity.badRequest().body("Malformed or Missing Session Context")
            );
        }

        // [STRUCTURAL CALLOUT] Geometric Tensor Veto (Edge Defense)
        // Physical Constraint: An AES-GCM payload cannot be mathematically decrypted
        // if it lacks the 12-byte nonce and 16-byte authentication tag. Vetoing here
        // prevents serialization and dispatch overhead across the enterprise bus.
        if (encryptedPayload == null || encryptedPayload.length < MINIMUM_GCM_ENVELOPE_BYTES) {
            final int length = (encryptedPayload == null) ? 0 : encryptedPayload.length;
            logger.error("SYPHER INTEGRITY FATAL: Payload length ({} bytes) violates minimum GCM envelope ({} bytes).",
                    length, MINIMUM_GCM_ENVELOPE_BYTES);
            return CompletableFuture.completedFuture(
                    ResponseEntity.badRequest().body("Invalid Payload Structure: Below Minimum Cryptographic Envelope")
            );
        }

        logger.debug("Ingested verified payload ({} bytes) for Session: {}", encryptedPayload.length, sessionId);

        // [STRUCTURAL CALLOUT] Asynchronous Kinetic Routing
        // Dispatches the payload to background worker pools, freeing the servlet
        // thread immediately to sustain high-volume ingress under adversarial conditions.
        return this.routingService.routeToPythonEngine(sessionId, encryptedPayload)
                .thenApply(ResponseEntity::ok)
                .exceptionally(ex -> {
                    // [STRUCTURAL CALLOUT] Cross-Stack Exception Boundary
                    // Masks internal stack traces and inter-process network diagnostics
                    // to prevent telemetry leakage to untrusted network clients.
                    logger.error("Inference routing failure for Session ID {}: {}", sessionId, ex.getMessage());
                    return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                            .body("Secure Inference Execution Failed");
                });
    }
}
