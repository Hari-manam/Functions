# Define a set of common stopwords
stopwords = {"the", "is", "in", "and", "to", "of", "a", "with", "for", "on"}

# Sample sentence
sentence = "The AI model is trained with large datasets for better accuracy."

# Convert sentence into words and remove stopwords
filtered_words = [word for word in sentence.lower().split() if word not in stopwords]

# Join the filtered words back into a sentence
cleaned_sentence = " ".join(filtered_words)

print("Original Sentence:", sentence)
print("Filtered Sentence:", cleaned_sentence)