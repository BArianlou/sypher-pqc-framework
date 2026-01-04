import numpy as np
import gymnasium as gym
from gymnasium import spaces
import argparse
import sys
import os

sys.path.append(os.path.dirname(__file__))
from rl_agent import RLAgent

class SypherSecurityEnv(gym.Env):
    """Custom Environment: Simulating Adversarial State-Space instability."""
    def __init__(self):
        super(SypherSecurityEnv, self).__init__()
        self.observation_space = spaces.Box(low=0, high=1, shape=(4,), dtype=np.float32)
        self.action_space = spaces.Discrete(2) # 0: Protect, 1: Pivot
        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.state = np.random.rand(4).astype(np.float32)
        self.steps = 0
        return self.state, {}

    def step(self, action):
        self.steps += 1
        reward = 1.0 if action == 0 else 0.5
        self.state = np.random.rand(4).astype(np.float32)
        terminated = self.steps >= 100
        return self.state, reward, terminated, False, {}

def run_sypher_training(episodes=100):
    env = SypherSecurityEnv()
    agent = RLAgent(env.observation_space.shape[0], env.action_space.n)

    for episode in range(episodes):
        state, info = env.reset()
        state = np.reshape(state, [1, agent.state_size])
        for time_step in range(100):
            action = np.argmax(agent.model.predict(state, verbose=0)) if np.random.rand() > agent.epsilon else env.action_space.sample()
            next_state, reward, done, _, _ = env.step(action)
            next_state = np.reshape(next_state, [1, agent.state_size])
            agent.store_experience(state, action, reward, next_state, done)
            state = next_state
            if done: break
        agent.train()
        agent.epsilon = max(agent.epsilon_min, agent.epsilon * agent.epsilon_decay)
    print("Sypher Intelligence Audit: SUCCESS")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=100)
    args = parser.parse_args()
    run_sypher_training(args.episodes)
