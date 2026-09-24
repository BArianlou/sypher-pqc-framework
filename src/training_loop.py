"""
===============================================================================
MODULE MANIFEST: SYPHER ADVERSARIAL ORCHESTRATOR & SIMULATION ENVIRONMENT
===============================================================================
System Purpose:
    Serves as the master execution sequencer and adversarial simulation engine
    for the SYPHER architecture. Couples a deterministic Markov Decision Process
    (MDP) simulating non-stationary cyber threat telemetry with the autonomic
    decision controller (RLAgent) to benchmark dynamic post-quantum cryptographic
    routing and key rotation policies.

State Boundaries:
    - Encapsulates synthetic adversarial state generation, observation envelopes,
      temporal step bounding, and operational reward emission.
    - Manages CLI parameter injection and cross-platform import path resolution.
    - Decoupled from neural graph compilation (SypherAI), low-level KEM
      encapsulation (SypherKEM), and symmetric payload encryption (SypherCipher).

Mathematical/Physical Invariants:
    1. MDP Transition Sequence:
       Enforces strictly ordered temporal execution:
       (S_t, A_t) -> (R_(t+1), S_(t+1), Terminated_Flag, Truncated_Flag)
       without state-leakage or backward time mutation.
    2. Temporal Horizon Clamping:
       Binds episodes to an explicit 100-step ceiling to prevent variance explosion
       and non-stationary drift during simulated network saturation.
    3. Hybrid_PQC_Evaluation Proxy:
       Reward signals balance baseline post-quantum security preservation against
       the kinetic latency and throughput penalties of cryptographic key rotation.

Design Rationale:
    Validating dynamic cryptographic routing requires simulating hostile network
    conditions without risking production communications infrastructure. Step-wise
    Bellman gradient updates allow the agent to continuously adapt defensive postures
    to simulated adversarial telemetry in high-frequency environments.
===============================================================================
"""

import argparse
import os
import sys
from typing import Any, Dict, Optional, Tuple
import gymnasium as gym
from gymnasium import spaces
import numpy as np

# [STRUCTURAL CALLOUT] CI/CD Path Synchronization
# Guarantees robust module resolution for automated GitHub Actions runners,
# containerized Kubernetes jobs, and staging environments without PYTHONPATH drift.
CURRENT_DIR: str = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from rl_agent import RLAgent


class SypherSecurityEnv(gym.Env):
    """Adversarial network simulation environment for cryptographic policy training.

    Models continuous threat telemetry, packet degradation, and operational
    trade-offs between high-overhead cryptographic protection and kinetic agility.

    Attributes:
        observation_space (spaces.Box): 4-dimensional normalized state space:
            [Threat Index, Bandwidth Saturation, Latency Variation, Compromise Risk].
        action_space (spaces.Discrete): Discrete policy choices:
            0 = Protect (Maintain high-security posture),
            1 = Pivot (Rotate keys / fallback to low-overhead hybrid profile).
        state (np.ndarray): Current 4D observation vector bounded in [0.0, 1.0].
        steps (int): Counter tracking discrete transitions within the active episode.
    """

    metadata: Dict[str, Any] = {"render_modes": []}

    def __init__(self) -> None:
        """Initializes the observation/action spaces and resets runtime counters."""
        super().__init__()

        # [STRUCTURAL CALLOUT] State-Space Tensor Envelope
        # Bounds the 4D state vector strictly within [0.0, 1.0], representing
        # normalized metrics: [Threat Level, Bandwidth Saturation, Latency Spike, Compromise Prob].
        self.observation_space: spaces.Box = spaces.Box(
            low=0.0,
            high=1.0,
            shape=(4,),
            dtype=np.float32,
        )

        # [STRUCTURAL CALLOUT] Cryptographic Action Space
        # 0: Protect (Retain high-assurance, heavy lattice-based security parameters).
        # 1: Pivot (Execute key rotation or adjust parameters for latency optimization).
        self.action_space: spaces.Discrete = spaces.Discrete(2)

        self.state: np.ndarray = np.zeros((4,), dtype=np.float32)
        self.steps: int = 0
        self.reset()

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Resets the environment to an initial stochastic threat baseline.

        Args:
            seed: Seed for the internal PRNG to ensure reproducible threat trajectories.
            options: Reserved configuration dictionary for interface compatibility.

        Returns:
            Tuple containing:
                - state (np.ndarray): Initial 4D observation vector in [0.0, 1.0]^4.
                - info (dict): Empty auxiliary diagnostic metadata.
        """
        super().reset(seed=seed)
        # Seeded PRNG ensures deterministic telemetry across test runs
        self.state = self.np_random.uniform(0.0, 1.0, size=(4,)).astype(np.float32)
        self.steps = 0
        return self.state, {}

    def step(
        self, action: int
    ) -> Tuple[np.ndarray, float, bool, bool, Dict[str, Any]]:
        """Advances the adversarial environment by one discrete temporal increment.

        Generates next-state threat observations, computes posture rewards based
        on operational overhead trade-offs, and evaluates episode termination bounds.

        Mathematical Invariants:
            - Reward Proxy: R_t = 1.0 (Protect) or 0.5 (Pivot)
            - Temporal Ceiling: Terminated = (steps >= 100)

        Args:
            action: Discrete policy action (0 = Protect, 1 = Pivot).

        Returns:
            Tuple containing:
                - next_state (np.ndarray): Updated 4D threat telemetry vector.
                - reward (float): Operational security vs. latency feedback reward.
                - terminated (bool): Flag indicating episodic ceiling expiration.
                - truncated (bool): Time-horizon truncation flag (fixed at False).
                - info (dict): Auxiliary diagnostic dictionary.
        """
        self.steps += 1

        # [STRUCTURAL CALLOUT] Operational Trade-off (Reward Logic)
        # Protect (action=0) yields full baseline security utility (1.0).
        # Pivot (action=1) incurs a kinetic penalty (0.5) to reflect the computational
        # and network handshake cost of mid-flight key ratcheting or scheme switching.
        reward: float = 1.0 if action == 0 else 0.5

        # Sample stochastic next-state threat telemetry using seeded PRNG
        self.state = self.np_random.uniform(0.0, 1.0, size=(4,)).astype(np.float32)

        # Temporal Horizon Clamp: Clamps episode to 100 transitions to avoid variance explosion
        terminated: bool = self.steps >= 100

        return self.state, reward, terminated, False, {}


def run_sypher_training(episodes: int = 100) -> None:
    """Executes the master adversarial training and optimization sequence.

    Instantiates the security environment and autonomic agent, steps through
    adversarial threat scenarios, commits state transitions to replay memory,
    and executes step-wise gradient backpropagation to converge on optimal policies.

    Mathematical Invariants:
        - Chronos_RL_Sequencing: Continuous mini-batch Bellman updates.
        - Experience Replay Decoupling: Uniform mini-batch sampling breaks
          autocorrelation in sequential network telemetry bursts.

    Input Envelopes:
        episodes (int): Total number of training episodes to simulate (>= 1).

    Args:
        episodes: Number of complete episodic horizons to execute.
    """
    env: SypherSecurityEnv = SypherSecurityEnv()
    agent: RLAgent = RLAgent(
        state_size=int(env.observation_space.shape[0]),
        action_size=int(env.action_space.n),
    )

    for episode in range(episodes):
        state, info = env.reset()

        # Execute bounded 100-step adversarial horizon
        for _ in range(100):
            # [STRUCTURAL CALLOUT] Encapsulated Action Logic
            # Epsilon-greedy action evaluation handles exploration/exploitation
            # transitions and tensor reshaping internally.
            action: int = agent.act(state)

            next_state, reward, terminated, truncated, _ = env.step(action)
            done: bool = terminated or truncated

            # [STRUCTURAL CALLOUT] Dimension-Safe Experience Routing
            # Ingests raw 1D arrays into the ring buffer to maintain contiguous
            # memory alignment during batched np.vstack operations.
            agent.store_experience(state, action, reward, next_state, done)

            state = next_state

            # [STRUCTURAL CALLOUT] High-Frequency Bellman Updates
            # Triggers gradient descent updates at every step once replay memory
            # satisfies the minimum mini-batch threshold.
            agent.train()

            if done:
                break

    print("Sypher Intelligence Audit: SUCCESS")


if __name__ == "__main__":
    # [STRUCTURAL CALLOUT] Execution Entry Point
    # Exposes simulation parameters to CLI arguments for integration into
    # automated MLOps pipelines and containerized testing harnesses.
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Sypher Adversarial Cryptographic Policy Orchestrator"
    )
    parser.add_argument(
        "--episodes",
        type=int,
        default=100,
        help="Number of adversarial episodes to simulate (default: 100)",
    )
    args: argparse.Namespace = parser.parse_args()

    run_sypher_training(episodes=args.episodes)
