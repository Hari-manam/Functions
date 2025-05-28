# 📘 Reinforcement Learning Complete Guide


## 1. What is Reinforcement Learning?

Reinforcement Learning (RL) is a type of machine learning where an **agent** learns how to make decisions by interacting with an **environment**. The goal is to **maximize cumulative rewards** over time.

💡 **Think of it like training a dog** – you reward good behavior and discourage bad behavior. Over time, the dog learns what gets a treat.

---

## 2. Why Reinforcement Learning?

RL is useful when:

* The data is sequential (time-based decisions)
* The right action isn’t always obvious immediately
* There's no labeled dataset (the agent learns by doing)

🎯 **Where is RL used?**

* Game AI (e.g., AlphaGo, Dota 2 bots)
* Self-driving cars
* Robotics and automation
* Dynamic pricing and portfolio optimization

---

## 3. Elements of Reinforcement Learning

* **Agent** – Learner (e.g., robot, AI bot)
* **Environment** – World in which the agent operates
* **State (s)** – Current situation or observation
* **Action (a)** – Choice made by the agent
* **Reward (r)** – Feedback from the environment
* **Policy (π)** – Strategy to pick actions
* **Value Function (V)** – Expected long-term reward from a state

🧠 **Why these elements?** They formalize how an agent behaves and learns from interaction.

---

## 4. Exploration vs Exploitation Dilemma

* **Exploration:** Try new actions to discover better rewards.
* **Exploitation:** Choose actions that gave high reward before.

📌 The **dilemma** is: Should the agent explore something new (which might be better), or exploit what it already knows?

---

## 5. Epsilon-Greedy Algorithm

This is the most common solution to the explore-exploit dilemma.

```python
if random.uniform(0, 1) < epsilon:
    action = env.action_space.sample()  # Explore
else:
    action = np.argmax(Q[state])       # Exploit
```

* `epsilon`: Probability of exploring (decays over time)
* Chooses best-known action most of the time, but occasionally explores

---

## 6. Markov Decision Process (MDP)

MDP is the math foundation for RL.
It assumes the **Markov property**: next state depends only on current state and action.

MDP = ⟨S, A, P, R, γ⟩

* **S**: States
* **A**: Actions
* **P**: Transition probabilities
* **R**: Rewards
* **γ**: Discount factor (future reward importance)

🔁 **Why MDP?** It models environments in a way we can compute optimal policies.

---

## 7. Q-values and V-values

* **Q(s,a):** Value of taking action `a` in state `s`
* **V(s):** Value of being in state `s` (maximum Q-value)

```python
V[s] = max(Q[s])
```

📌 **Why Q-values?** They guide the agent in picking actions. V-values summarize the best possible outcome from a state.

---

## 8. Alpha (α) - Learning Rate

Alpha (α) controls how quickly the agent learns new information:

* High α → quick learning but unstable
* Low α → stable but slow learning

```python
Q[s,a] = Q[s,a] + α * (reward + γ * max(Q[s']) - Q[s,a])
```

🧠 The formula updates our belief about how good it is to take `a` in `s`.

---

## 9. Full Code Example: Q-Learning on FrozenLake

```python
import numpy as np
import gym
import random

env = gym.make("FrozenLake-v1", is_slippery=True)
Q = np.zeros((env.observation_space.n, env.action_space.n))

episodes = 1000
alpha = 0.8
gamma = 0.95
epsilon = 1.0
decay = 0.995
min_epsilon = 0.01

for episode in range(episodes):
    state = env.reset()[0]
    done = False

    while not done:
        if random.uniform(0,1) < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(Q[state])

        next_state, reward, done, _, _ = env.step(action)
        Q[state, action] += alpha * (reward + gamma * np.max(Q[next_state]) - Q[state, action])
        state = next_state

    epsilon = max(min_epsilon, epsilon * decay)

# Evaluation
for _ in range(5):
    state = env.reset()[0]
    done = False
    while not done:
        env.render()
        action = np.argmax(Q[state])
        state, _, done, _, _ = env.step(action)
```

