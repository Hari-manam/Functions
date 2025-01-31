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

# auto recommender system

users = {
    "Alice": {"Laptop", "Mouse"},
    "Bob": {"Laptop", "Keyboard"},
}

def recommend(user):
    return set().union(*users.values()) - users[user]

print(recommend("Alice"))  # Output: {'Keyboard'}

# Removing the duplicates 

def remove_duplicates(lst):
    return list(set(lst))

data = [1, 2, 2, 3, 4, 4, 5, 6, 6]
unique_data = remove_duplicates(data)

print(unique_data)  # Output: [1, 2, 3, 4, 5, 6]

# finding disease systems 

# Define symptoms for different diseases
diseases = {
    "Flu": {"fever", "cough", "fatigue", "body ache"},
    "Cold": {"cough", "sneezing", "runny nose"},
    "COVID-19": {"fever", "cough", "loss of taste", "fatigue"},
    "Allergy": {"sneezing", "runny nose", "itchy eyes"}
}

# Function to find possible diseases based on symptoms
def find_disease(symptoms):
    possible_diseases = {disease for disease, sym_set in diseases.items() if symptoms & sym_set}
    return possible_diseases or {"No match found"}

# Example: Finding possible diseases for a patient with symptoms
patient_symptoms = {"fever", "cough"}
possible_diseases = find_disease(patient_symptoms)

print(f"Possible diseases: {possible_diseases}")