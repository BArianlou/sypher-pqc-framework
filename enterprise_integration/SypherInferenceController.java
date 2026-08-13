package com.sypher.enterprise.api;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.concurrent.CompletableFuture;

/**
 * SYPHER ENTERPRISE INTEGRATION LAYER
 * Architecture: Spring Boot REST Controller
 * Purpose: Acts as the secure Java gateway between the enterprise backend 
 * and the Python-based Sypher Cryptographic & ML Inference engines.
 */
@RestController
@RequestMapping("/api/v1/sypher")
public class SypherInferenceController {

    private static final Logger logger = LoggerFactory.getLogger(SypherInferenceController.class);
    
    // In a full deployment, this service routes payloads to the Python gRPC/REST backend
    private final SypherRoutingService routingService;

    public SypherInferenceController(SypherRoutingService routingService) {
        this.routingService = routingService;
    }

    @PostMapping("/secure-inference")
    public CompletableFuture<ResponseEntity<String>> processSecurePayload(
            @RequestHeader("X-Session-ID") String sessionId,
            @RequestBody byte[] encryptedPayload) {
        
        logger.info("Received encrypted inference request for Session ID: {}", sessionId);

        // Fail-Safe: Reject malformed payloads before they hit the ML engine
        if (encryptedPayload == null || encryptedPayload.length < 12) {
            logger.error("SYPHER INTEGRITY FATAL: Payload too short to contain valid GCM nonce.");
            return CompletableFuture.completedFuture(ResponseEntity.badRequest().body("Invalid Payload Structure"));
        }

        // Asynchronous routing to the Python ML backend to prevent Java thread-blocking
        return routingService.routeToPythonEngine(sessionId, encryptedPayload)
                .thenApply(ResponseEntity::ok)
                .exceptionally(ex -> {
                    logger.error("Inference routing failed: {}", ex.getMessage());
                    return ResponseEntity.internalServerError().body("Secure Inference Failed");
                });
    }
}
