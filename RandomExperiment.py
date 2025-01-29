import random

N = 10  # Number of experiments
choices = ["Red", "Blue"]
count = {"Red": 0, "Blue": 0}

for _ in range(N):
    picks = [random.choice(choices) for _ in range(2)]  # Pick 2 balls
    for pick in picks:
        count[pick] += 1  # Count occurrences of each color

# Calculating probabilities
total_picks = 2 * N  # Total picks across all experiments
for ball, freq in count.items():
    print(f"Probability of picking {ball}: {freq / total_picks:.4f}")