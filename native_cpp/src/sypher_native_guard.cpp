/**
 * ===============================================================================
 * MODULE MANIFEST: SYPHER NATIVE GUARD IMPLEMENTATION (LOCK-FREE CORE)
 * ===============================================================================
 * System Purpose:
 *     Executes the hardware-level veto gate and memory management for the SYPHER
 *     engine. Implements the O(1) validation pipeline that intercepts, sanitizes,
 *     and commits cryptographic routing actions directly to the CPU cache without
 *     incurring kernel-level context switches or OS thread preemption.
 *
 * State Boundaries:
 *     - Strictly confined to atomic register operations and L1/L2 cache coherency.
 *     - Delegates all high-order mathematical derivations to the Python/TensorFlow
 *       layers, acting solely as the deterministic physical execution boundary.
 *
 * Mathematical/Physical Invariants:
 *     1. Bayesian_Dampener:
 *        max_variance_bound_ is physically enforced to clamp state-space volatility,
 *        triggering Structural_Veto_Gate (transition_prob_ij = 0.0) on breach.
 *     2. Bitwise Index Masking Invariant:
 *        Index = Action_ID & BUFFER_MASK, where BUFFER_MASK = BUFFER_SIZE - 1.
 *        Guarantees zero-drag, O(1) ring buffer slot allocation.
 *     3. Release-Acquire Memory Order:
 *        Release-store on timestamp_ns guarantees that relaxed stores to action_id
 *        and action_value are globally visible prior to timestamp validation.
 *
 * Design Rationale:
 *     Standard OS-level locking (e.g., std::mutex) introduces non-deterministic
 *     context switches and thread suspension latency. This native C++20
 *     implementation utilizes explicit memory-ordered atomics to maintain
 *     deterministic sub-microsecond validation velocity during high-frequency
 *     adversarial engagements.
 * ===============================================================================
 */

#include "sypher_native_guard.hpp"
#include <chrono>
#include <cmath>

namespace sypher::native {

/**
 * @brief Constructs the native guard instance, establishing hardware boundary thresholds.
 *
 * @param max_variance_bound The absolute mathematical ceiling for state variance.
 * @param min_entropy_threshold The exploration entropy floor.
 */
SypherNativeGuard::SypherNativeGuard(double max_variance_bound, double min_entropy_threshold) noexcept
    : max_variance_bound_(max_variance_bound),
      min_entropy_threshold_(min_entropy_threshold) {}

/**
 * @brief Evaluates an incoming cryptographic action against hardware bounds.
 *
 * Validates state variance against max_variance_bound_, checks action utility
 * for non-finite values (NaN/Inf), and commits the record to the circular buffer
 * via a release-store memory fence.
 *
 * @param action_id Monotonically increasing identifier of the candidate action.
 * @param action_value Continuous Q-value or utility assigned to the action.
 * @param state_variance Empirical variance of the incoming telemetry batch.
 * @return true if the action cleared all boundary gates; false if vetoed.
 */
bool SypherNativeGuard::validate_and_clamp_action(
    uint64_t action_id,
    double action_value,
    double state_variance
) noexcept {

    // [STRUCTURAL CALLOUT] Bayesian Dampener Enforcement
    // Mathematical Invariant: Maps to max_variance_bound_. Extreme volatility
    // or adversarial telemetry bursts exceeding this bound trigger an immediate
    // hardware veto (Structural_Veto_Gate: transition_prob_ij = 0.0).
    if (state_variance > max_variance_bound_) {
        return false;
    }

    // [STRUCTURAL CALLOUT] Geometric Tensor Sanitization
    // Physical Constraint: Deep Q-Networks can emit NaN or +/-Inf during gradient
    // anomalies. This hardware gate catches floating-point degeneracies, preventing
    // mathematical corruption from penetrating the native C++ memory space.
    if (std::isnan(action_value) || std::isinf(action_value)) {
        return false;
    }

    // [STRUCTURAL CALLOUT] Bitwise Kinetic Routing
    // Mathematical Invariant: BUFFER_SIZE is an exact power of two (1024), so
    // bitwise AND with BUFFER_MASK (1023) replaces the integer modulo (%) operator.
    // This eliminates division latency, bypassing the CPU ALU divider unit.
    const std::size_t index = static_cast<std::size_t>(action_id & BUFFER_MASK);
    auto& slot = ring_buffer_[index];

    // High-resolution monotonic timestamp for temporal provenance logging
    const uint64_t now_ns = static_cast<uint64_t>(
        std::chrono::duration_cast<std::chrono::nanoseconds>(
            std::chrono::high_resolution_clock::now().time_since_epoch()
        ).count()
    );

    // [STRUCTURAL CALLOUT] Lock-Free Memory Coherency
    // Enforces explicit hardware memory ordering:
    // std::memory_order_relaxed: Writes action_id and action_value into the L1/L2
    // cache without invoking expensive cross-core synchronization barriers.
    // std::memory_order_release: Stores timestamp_ns with release semantics,
    // establishing a memory barrier that guarantees prior writes are visible
    // to any thread performing an acquire-load on timestamp_ns.
    slot.action_id.store(action_id, std::memory_order_relaxed);
    slot.action_value.store(action_value, std::memory_order_relaxed);
    slot.timestamp_ns.store(now_ns, std::memory_order_release);

    return true;
}

} // namespace sypher::native
