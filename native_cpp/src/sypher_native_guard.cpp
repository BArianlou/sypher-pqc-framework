#include "sypher_native_guard.hpp"
#include <chrono>

namespace sypher::native {

SypherNativeGuard::SypherNativeGuard(double max_variance_bound, double min_entropy_threshold) noexcept
    : max_variance_bound_(max_variance_bound),
      min_entropy_threshold_(min_entropy_threshold) {}

bool SypherNativeGuard::validate_and_clamp_action(uint64_t action_id, double action_value, double state_variance) noexcept {
    // Check 1: Invariant Variance Clamping
    if (state_variance > max_variance_bound_) {
        return false;
    }

    // Check 2: Non-finite Value Guard (NaN / Infinity check)
    if (std::isnan(action_value) || std::isinf(action_value)) {
        return false;
    }

    // Lock-free, zero-allocation ring buffer indexing
    const size_t index = action_id & (BUFFER_SIZE - 1);
    auto& slot = ring_buffer_[index];

    const uint64_t now_ns = static_cast<uint64_t>(
        std::chrono::duration_cast<std::chrono::nanoseconds>(
            std::chrono::high_resolution_clock::now().time_since_epoch()
        ).count()
    );

    // Atomic update without heap allocation or mutex locking
    slot.action_id.store(action_id, std::memory_order_relaxed);
    slot.action_value.store(action_value, std::memory_order_relaxed);
    slot.timestamp_ns.store(now_ns, std::memory_order_release);

    return true;
}

} // namespace sypher::native
