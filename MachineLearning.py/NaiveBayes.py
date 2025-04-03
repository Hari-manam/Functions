import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score

# Set random seed for reproducibility
np.random.seed(42)

# --- 1. Gaussian Naive Bayes (Iris Dataset) ---
print("=== Gaussian Naive Bayes (Iris Dataset) ===")
# Load dataset
iris = load_iris()
X_iris = iris.data  # Continuous features
y_iris = iris.target  # Classes: 0, 1, 2

# Split data
X_train_iris, X_test_iris, y_train_iris, y_test_iris = train_test_split(
    X_iris, y_iris, test_size=0.3, random_state=42
)

# Train model
gnb = GaussianNB()
gnb.fit(X_train_iris, y_train_iris)

# Predict and evaluate
y_pred_iris = gnb.predict(X_test_iris)
gnb_accuracy = accuracy_score(y_test_iris, y_pred_iris)
print(f"Accuracy: {gnb_accuracy:.2f}")

# Visualization: Simple Bar Chart of Correct Predictions
correct_iris = np.sum(y_pred_iris == y_test_iris)
total_iris = len(y_test_iris)
plt.figure(figsize=(5, 3))
plt.bar(["Correct"], [correct_iris], color="#66CC99", width=0.4)
plt.ylim(0, total_iris)
plt.title("Gaussian NB: Correct Predictions")
plt.ylabel("Number of Flowers")
plt.text(0, correct_iris + 1, f"{correct_iris}/{total_iris}", ha="center")
plt.show()
print("Bar Chart: Shows how many flowers were predicted correctly out of the total test set.")

# --- 2. Multinomial Naive Bayes (Text Sentiment) ---
print("\n=== Multinomial Naive Bayes (Text Sentiment) ===")
# Synthetic text dataset
texts = [
    "I love this movie great acting",
    "Terrible film waste of time",
    "Amazing plot and characters",
    "Boring and dull story",
    "Fantastic direction and visuals",
    "Awful script bad ending"
]
labels = [1, 0, 1, 0, 1, 0]  # 1 = Positive, 0 = Negative

# Convert text to word count matrix
vectorizer_mnb = CountVectorizer()
X_text = vectorizer_mnb.fit_transform(texts)

# Split data
X_train_text, X_test_text, y_train_text, y_test_text = train_test_split(
    X_text, labels, test_size=0.3, random_state=42
)

# Train model
mnb = MultinomialNB()
mnb.fit(X_train_text, y_train_text)

# Predict and evaluate
y_pred_text = mnb.predict(X_test_text)
mnb_accuracy = accuracy_score(y_test_text, y_pred_text)
print(f"Accuracy: {mnb_accuracy:.2f}")

# Visualization: Simple Bar Chart of Correct Predictions
correct_text = np.sum(y_pred_text == y_test_text)
total_text = len(y_test_text)
plt.figure(figsize=(5, 3))
plt.bar(["Correct"], [correct_text], color="#66CC99", width=0.4)
plt.ylim(0, total_text)
plt.title("Multinomial NB: Correct Predictions")
plt.ylabel("Number of Reviews")
plt.text(0, correct_text + 0.1, f"{correct_text}/{total_text}", ha="center")
plt.show()
print("Bar Chart: Shows how many reviews were predicted correctly out of the total test set.")

# --- 3. Bernoulli Naive Bayes (Spam Detection) ---
print("\n=== Bernoulli Naive Bayes (Spam Detection) ===")
# Synthetic email dataset
emails = [
    "win free money now",
    "meeting at noon tomorrow",
    "claim your prize today",
    "hello how are you",
    "free offer click here",
    "work discussion later"
]
labels = [1, 0, 1, 0, 1, 0]  # 1 = Spam, 0 = Not Spam

# Convert text to binary matrix
vectorizer_bnb = CountVectorizer(binary=True)
X_email = vectorizer_bnb.fit_transform(emails)

# Split data
X_train_email, X_test_email, y_train_email, y_test_email = train_test_split(
    X_email, labels, test_size=0.3, random_state=42
)

# Train model
bnb = BernoulliNB()
bnb.fit(X_train_email, y_train_email)

# Predict and evaluate
y_pred_email = bnb.predict(X_test_email)
bnb_accuracy = accuracy_score(y_test_email, y_pred_email)
print(f"Accuracy: {bnb_accuracy:.2f}")

# Visualization: Simple Bar Chart of Correct Predictions
correct_email = np.sum(y_pred_email == y_test_email)
total_email = len(y_test_email)
plt.figure(figsize=(5, 3))
plt.bar(["Correct"], [correct_email], color="#66CC99", width=0.4)
plt.ylim(0, total_email)
plt.title("Bernoulli NB: Correct Predictions")
plt.ylabel("Number of Emails")
plt.text(0, correct_email + 0.1, f"{correct_email}/{total_email}", ha="center")
plt.show()
print("Bar Chart: Shows how many emails were predicted correctly out of the total test set.")

# --- Example Predictions ---
print("\n=== Example Predictions ===")
new_iris = [[5.0, 3.4, 1.5, 0.2]]
print(f"Gaussian NB Prediction: {iris.target_names[gnb.predict(new_iris)[0]]}")

new_text = ["This movie is awesome"]
X_new_text = vectorizer_mnb.transform(new_text)
print(f"Multinomial NB Prediction: {'Positive' if mnb.predict(X_new_text)[0] == 1 else 'Negative'}")

new_email = ["win a free trip"]
X_new_email = vectorizer_bnb.transform(new_email)
print(f"Bernoulli NB Prediction: {'Spam' if bnb.predict(X_new_email)[0] == 1 else 'Not Spam'}")