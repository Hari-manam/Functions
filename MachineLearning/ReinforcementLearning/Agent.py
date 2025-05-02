import numpy as np
import gymnasium as gym
import random

# 1. Problem Definition
env = gym.make("FrozenLake-v1", is_slippery=True)  # 4x4 grid with slippery moves
state_space = env.observation_space.n              # 16 states
action_space = env.action_space.n                  # 4 actions (left, down, right, up)

# 2. Q-table Initialization
Q = np.zeros((state_space, action_space))          # Q-table: state x action

# 3. Hyperparameters
episodes = 1000
max_steps = 100           # per episode
learning_rate = 0.8       # α
discount_factor = 0.95    # γ
epsilon = 1.0             # exploration rate
min_epsilon = 0.01
decay_rate = 0.995        # decay epsilon after each episode

# 4. Training Phase
for episode in range(episodes):
    state = env.reset()[0]   # get initial state
    done = False

    for step in range(max_steps):
        # Epsilon-greedy: choose action
        if random.uniform(0, 1) < epsilon:
            action = env.action_space.sample()  # explore
        else:
            action = np.argmax(Q[state])        # exploit best-known action

        # Take action → get reward and next state
        next_state, reward, done, _, _ = env.step(action)

        # Update Q-value using Q-learning formula
        old_value = Q[state, action]
        next_max = np.max(Q[next_state])
        Q[state, action] = old_value + learning_rate * (reward + discount_factor * next_max - old_value)

        state = next_state

        if done:
            break

    # Decay epsilon after each episode
    epsilon = max(min_epsilon, epsilon * decay_rate)

# 5. Evaluation Phase
print("\n--- Evaluation after Training ---\n")
successes = 0
for episode in range(10):
    state = env.reset()[0]
    done = False
    print(f"Episode {episode + 1}:")

    for step in range(max_steps):
        env.render()
        action = np.argmax(Q[state])
        new_state, reward, done, _, _ = env.step(action)
        state = new_state
        if done:
            if reward == 1:
                successes += 1
            print("✔️ Reached Goal!" if reward == 1 else "❌ Fell in a hole.")
            break

print(f"\nSuccess rate: {successes}/10")
env.close()
