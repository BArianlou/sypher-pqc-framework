#ifndef SYPHER_NATIVE_GUARD_HPP
#define SYPHER_NATIVE_GUARD_HPP

#include <atomic>
#include <cstdint>
#include <cmath>
#include <array>

namespace sypher::native {

/**
 * @brief Zero-allocation state-space action container for high-frequency execution.
 * alignas(64) prevents false sharing across CPU cache lines.
 */
struct alignas(64) ActionPayload {
    std::atomic<uint64_t> action_id{0};
    std::atomic<double> action_value{0.0};
    std::atomic<uint64_t> timestamp_ns{0};
};

/**
 * @brief Ultra-low latency Native Guard Protocol.
 * Enforces invariant state-space boundary clamping directly at the C++ memory level.
 */
class SypherNativeGuard {
public:
    explicit SypherNativeGuard(double max_variance_bound, double min_entropy_threshold) noexcept;

    // Disallow copy/move to enforce fixed memory alignment
    SypherNativeGuard(const SypherNativeGuard&) = delete;
    SypherNativeGuard& operator=(const SypherNativeGuard&) = delete;

    /**
     * @brief Clamps and validates policy action vectors under zero-allocation constraints.
     */
    [[nodiscard]] bool validate_and_clamp_action(uint64_t action_id, double action_value, double state_variance) noexcept;

private:
    static constexpr size_t BUFFER_SIZE = 1024;
    alignas(64) std::array<ActionPayload, BUFFER_SIZE> ring_buffer_{};
    
    const double max_variance_bound_;
    const double min_entropy_threshold_;
};

} // namespace sypher::native

#endif // SYPHER_NATIVE_GUARD_HPP
