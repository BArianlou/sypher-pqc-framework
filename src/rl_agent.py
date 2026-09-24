"""
===============================================================================
MODULE MANIFEST: SYPHER AUTONOMIC AGENT (ADVERSARIAL RL CORE)
===============================================================================
System Purpose:
    Serves as the sovereign execution controller for the SYPHER cryptographic
    routing engine. Orchestrates autonomic feedback loops to dynamically select
    cryptographic schemes and key encapsulation parameters under adversarial
    network regimes. Balances post-quantum security guarantees against real-world
    latency overhead, packet size, and bandwidth constraints.

State Boundaries:
    - Governs episodic adversarial experience ingestion, ring-buffer replay memory,
      and dynamic security policy exploitation.
    - Encapsulates exploration schedules and Bellman TD-error target calculations.
    - Strictly delegates neural graph compilation, gradient backpropagation,
      and Huber loss optimization to the SypherAI backbone.

Mathematical/Physical Invariants:
    1. Hybrid_PQC_Evaluation:
       Viability_Score = (Security_Level * w1) - (Latency_Overhead * w2) - (Size_Overhead * w3)
       Forms the core scalar reward signal driving policy convergence.
    2. Chronos_RL_Sequencing:
       Q(s, a) <- Q(s, a) + alpha * [Reward + gamma * max_a' Q(s', a') - Q(s, a)]
       Optimizes long-term security posture under non-stationary attack surfaces.
    3. Monotonic Entropy Decay:
       Exploration rate epsilon decays strictly monotonically:
       epsilon_(t+1) = max(epsilon_min, epsilon_t * epsilon_decay)
       driving transitions from exploratory scheme evaluation to deterministic
       cryptographic selection.

Design Rationale:
    Static cipher assignment in untrusted networks creates single-point cryptographic
    vulnerabilities during harvest-now, decrypt-later threats or sudden bandwidth
    degradation. Experience Replay breaks temporal correlation across sequential
    telemetry bursts, while batched tensor operations minimize kinetic latency
    in high-frequency enterprise communication buses.
===============================================================================
"""

from collections import deque
import random
from typing import Deque, List, Tuple
import numpy as np
import tensorflow as tf

from sypher_ai import SypherAI


class RLAgent:
    """Autonomic Deep Q-Network (DQN) agent for adaptive post-quantum routing.

    Balances cryptographic security levels against transport-layer latency and
    bandwidth costs using an adversarial reinforcement learning control loop.

    Attributes:
        state_size (int): Dimensionality of the network and threat observation vector.
        action_size (int): Cardinality of discrete cryptographic policy primitives.
        memory (Deque[Tuple[np.ndarray, int, float, np.ndarray, bool]]): Cyclic
            replay buffer storing adversarial state-transition tuples.
        gamma (float): Discount factor for future expected security/performance yields.
        epsilon (float): Dynamic probability threshold for exploratory policy selection.
        epsilon_min (float): Lower bound floor on exploration probability.
        epsilon_decay (float): Multiplicative decay rate applied to epsilon per update.
        model (tf.keras.Model): Compiled Q-value approximator graph from SypherAI.
    """

    def __init__(self, state_size: int, action_size: int) -> None:
        """Initializes the RLAgent parameters, replay queue, and policy backbone.

        Args:
            state_size: Dimensionality of the incoming observation state tensor
                (e.g., threat indicator, network RTT, packet loss, cipher overhead).
            action_size: Number of discrete cryptographic configurations available
                (e.g., Classical X25519, ML-KEM-512, ML-KEM-768, ML-KEM-1024, hybrid mode).
        """
        self.state_size: int = state_size
        self.action_size: int = action_size

        # [STRUCTURAL CALLOUT] Finite Memory Horizon
        # Physical Constraint: Caps replay memory at 2000 transitions.
        # Operates as a FIFO ring-buffer to prevent training on stale network
        # topologies or outdated adversarial threat vectors.
        self.memory: Deque[Tuple[np.ndarray, int, float, np.ndarray, bool]] = deque(maxlen=2000)

        self.gamma: float = 0.95
        self.epsilon: float = 1.0
        self.epsilon_min: float = 0.01
        self.epsilon_decay: float = 0.995

        # Instantiates the underlying neural network backbone
        self.model: tf.keras.Model = SypherAI(state_size, action_size).model

    def store_experience(
        self,
        state: np.ndarray,
        action: int,
        reward: float,
        next_state: np.ndarray,
        done: bool,
    ) -> None:
        """Appends a discrete state transition tuple to the FIFO replay buffer.

        Args:
            state: Pre-transition observation vector of shape (state_size,).
            action: Discrete cryptographic primitive selected in range [0, action_size - 1].
            reward: Scalar feedback derived from the Hybrid_PQC_Evaluation equation.
            next_state: Post-transition observation vector of shape (state_size,).
            done: Terminal boundary indicator (e.g., successful transmission, fatal compromise).
        """
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state: np.ndarray) -> int:
        """Selects a cryptographic configuration primitive via an epsilon-greedy policy.

        Mathematical Invariants:
            - Exploration Probability: P(a = random) = epsilon
            - Exploitation Probability: P(a = argmax_a Q(s, a)) = 1 - epsilon

        Args:
            state: Current network telemetry and threat observation vector.

        Returns:
            int: Discrete action primitive representing the selected cryptographic scheme.
        """
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)

        # [STRUCTURAL CALLOUT] Dimension-Safe Tensor Reshaping
        # Dynamically projects 1D observations into a 2D batch shape (1, state_size)
        # to satisfy Keras graph input requirements without mutating underlying data.
        state_tensor: np.ndarray = (
            np.reshape(state, (1, self.state_size)) if state.ndim == 1 else state
        )
        q_values: np.ndarray = self.model.predict(state_tensor, verbose=0)
        return int(np.argmax(q_values[0]))

    def train(self, batch_size: int = 32) -> None:
        """Performs a mini-batch gradient descent update on the Q-network.

        Samples decorrelated transitions from the memory buffer, derives Bellman
        target Q-values using the Hybrid_PQC_Evaluation feedback, and updates network weights.

        Mathematical Invariants:
            - Terminal Step: Target Q(s_t, a_t) = r_t
            - Non-Terminal Step: Target Q(s_t, a_t) = r_t + gamma * max_a' Q(s_(t+1), a')
            - Monotonic Entropy Decay: epsilon <- max(epsilon_min, epsilon * epsilon_decay)

        Args:
            batch_size: Minimum transition threshold required to trigger gradient descent.
        """
        if len(self.memory) < batch_size:
            return

        batch: List[Tuple[np.ndarray, int, float, np.ndarray, bool]] = random.sample(
            self.memory, batch_size
        )

        # [STRUCTURAL CALLOUT] Triune Vectorization & Kinetic Speedup
        # Stacks sampled transition tuples into contiguous memory buffers to
        # leverage SIMD/GPU parallelization across batch inference passes.
        states: np.ndarray = np.vstack([x[0] for x in batch])
        actions: np.ndarray = np.array([x[1] for x in batch], dtype=np.int32)
        rewards: np.ndarray = np.array([x[2] for x in batch], dtype=np.float32)
        next_states: np.ndarray = np.vstack([x[3] for x in batch])
        dones: np.ndarray = np.array([x[4] for x in batch], dtype=bool)

        # Batched inference for current and next-state Q-distributions
        target_values: np.ndarray = self.model.predict(states, verbose=0)
        next_q_values: np.ndarray = self.model.predict(next_states, verbose=0)

        # [STRUCTURAL CALLOUT] Vectorized Bellman Target Update
        # Direct implementation of Chronos_RL_Sequencing for adversarial policy convergence.
        for i in range(batch_size):
            if dones[i]:
                target_values[i, actions[i]] = rewards[i]
            else:
                target_values[i, actions[i]] = rewards[i] + self.gamma * float(
                    np.max(next_q_values[i])
                )

        # Gradient update on batched targets
        self.model.fit(
            states, target_values, batch_size=batch_size, epochs=1, verbose=0
        )

        # [STRUCTURAL CALLOUT] Triune Entropy Decay
        # Decays exploration entropy toward epsilon_min to converge on stable routing policies.
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
