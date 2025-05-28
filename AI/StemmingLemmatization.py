import fitz  # PyMuPDF
import re
import pandas as pd
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import wordnet
import nltk

# Download required NLTK resources
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

# -------- STEP 1: Load and Read PDF --------
pdf_path = "N:\State-of-AI-Report-2023.pdf"  
doc = fitz.open(pdf_path)

full_text = ""
for page in doc:
    full_text += page.get_text()

# -------- STEP 2: Preprocess and Tokenize --------
text = full_text.lower()
words = re.findall(r'\b[a-z]+\b', text)  # Extract alphabetic words only
unique_words = sorted(set(words))  # Remove duplicates

# -------- STEP 3: NLP Setup --------
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

# -------- STEP 4: Process Each Word --------
data = []
for word in unique_words:
    lemma = lemmatizer.lemmatize(word)
    stem = stemmer.stem(word)
    senses = wordnet.synsets(word)
    is_ambiguous = len(senses) > 1
    data.append({
        "Original Word": word,
        "Lemmatized": lemma,
        "Stemmed": stem,
        "Is Ambiguous": is_ambiguous
    })

# -------- STEP 5: Create DataFrame --------
df = pd.DataFrame(data)
print(df.head(20))  # Show top 20 rows

# -------- STEP 6: Optional Save --------
df.to_csv("word_lemmatization_stemming_ambiguity.csv", index=False)
