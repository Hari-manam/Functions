
import fitz  # PyMuPDF
import nltk
import matplotlib.pyplot as plt
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from sklearn.feature_extraction.text import CountVectorizer
import re

# ✅ Step 1: Load PDF using PyMuPDF
doc = fitz.open("N:\State-of-AI-Report-2023.pdf")  # Use your actual filename
text = ""
for page in doc:
    text += page.get_text()

# ✅ Step 2: Clean the text
cleaned_text = re.sub(r'[^a-zA-Z\s]', '', text)
cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
cleaned_text = cleaned_text.lower()

# ✅ Step 3: Tokenization
nltk.download('punkt')
tokens = word_tokenize(cleaned_text)

# ✅ Step 4: Bag of Words
bow = Counter(tokens)
print("Top 10 Words:", bow.most_common(10))

# ✅ Step 5: CountVectorizer N-grams
vectorizer = CountVectorizer(ngram_range=(1, 3))
X = vectorizer.fit_transform([cleaned_text])
features = vectorizer.get_feature_names_out()
print("Vectorized Features:", features[:10])

# ✅ Step 6: Plot Top Words
top_words = bow.most_common(10)
words = [w for w, c in top_words]
counts = [c for w, c in top_words]
plt.figure(figsize=(10, 5))
plt.bar(words, counts, color='skyblue')
plt.title("Top 10 Words in State of AI Report 2023")
plt.xlabel("Words")
plt.ylabel("Frequency")
plt.grid(True)
plt.show()
