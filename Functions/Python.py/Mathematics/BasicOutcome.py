def probability(sample_space, event):
    return sample_space.count(event) / len(sample_space) if event in sample_space else 0

sample_space =["heads", "tails"]
event = "heads"

print(f"probability of '{event}': {probability(sample_space, event):.2f}")