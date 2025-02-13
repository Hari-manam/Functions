def grocery_probability():
    sample_space = ["chocolates", "pencil", "chips", "biscuits"]
    total_items = len(sample_space)
    
    # Probability of selecting pencil or chips
    selected_items = ["pencil", "chips"]
    probability = len(selected_items) / total_items
    
    return probability

# Print the probability
print(f"Probability of selecting a pencil or chips: {grocery_probability():.2f}")