import fitz  # PyMuPDF
import re
from collections import Counter
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# -------- STEP 1: Load and Read PDF --------
pdf_path = "N:\State-of-AI-Report-2023.pdf"  # Replace with your file path
doc = fitz.open(pdf_path)

# Extract text from all pages
full_text = ""
for page in doc:
    full_text += page.get_text()

# -------- STEP 2: Preprocess Text --------
# Split text into sentences (basic)
sentences = re.split(r'(?<=[.!?]) +', full_text)
sentences = [s.strip().replace('\n', ' ') for s in sentences if len(s.strip().split()) > 4]

# Join all sentences for full-document term frequency
document = " ".join(sentences).lower()
words = re.findall(r'\b\w+\b', document)

# -------- STEP 3: Compute TF (Term Frequency) --------
total_terms = len(words)
tf_counter = Counter(words)
tf = {word: count / total_terms for word, count in tf_counter.items()}

# -------- STEP 4: Compute IDF (Inverse Document Frequency) --------
vectorizer = TfidfVectorizer()
vectorizer.fit(sentences)  # Uses sentences to compute IDF
idf = dict(zip(vectorizer.get_feature_names_out(), vectorizer.idf_))

# -------- STEP 5: Compute TF-IDF --------
tf_idf = {word: tf.get(word, 0) * idf.get(word, 0) for word in vectorizer.get_feature_names_out()}

# -------- STEP 6: Format Results into DataFrame --------
words_sorted = sorted(tf_idf.items(), key=lambda x: x[1], reverse=True)
final_data = [{
    "Word": word,
    "Term Frequency": round(tf.get(word, 0), 6),
    "Inverse Document Frequency": round(idf.get(word, 0), 6),
    "TF-IDF": round(score, 6)
} for word, score in words_sorted]

df = pd.DataFrame(final_data)

# -------- STEP 7: Display or Export --------
print(df.head(20))  # Show top 20 words

# Optional: Save as CSV
df.to_csv("tfidf_results.csv", index=False)
