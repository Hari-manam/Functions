import pandas as pd
import re
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk import word_tokenize
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns

# First-time setup (only needed once)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load CSV
df = pd.read_csv(r"N:\combined_youtube_comments.csv")
df = df.dropna()
comments = df['comment'].astype(str).tolist()

# Tools
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
stop_words = set(stopwords.words("english"))
homophones = {"2": "to", "too": "to", "u": "you", "ur": "your", "r": "are"}

# Processing pipeline
results = []

for text in comments:
    original = text
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    tokens = word_tokenize(text)
    tokens = [homophones.get(w, w) for w in tokens if w not in stop_words]
    lemmas = [lemmatizer.lemmatize(w) for w in tokens]
    stems = [stemmer.stem(w) for w in tokens]
    homonyms = {w: wordnet.synsets(w)[0].definition() for w in tokens if len(wordnet.synsets(w)) > 1}
    sentiment_score = TextBlob(" ".join(tokens)).sentiment.polarity
    if sentiment_score > 0.1:
        sentiment = "Positive"
    elif sentiment_score < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    results.append({
        "original": original,
        "cleaned": " ".join(tokens),
        "lemmas": lemmas,
        "stems": stems,
        "homonyms": homonyms,
        "sentiment_score": sentiment_score,
        "sentiment_label": sentiment
    })

# Save results
processed_df = pd.DataFrame(results)
processed_df.to_csv("processed_youtube_comments_full.csv", index=False)
print("✅ All results saved to processed_youtube_comments_full.csv")

# Plot sentiment breakdown
sentiment_counts = processed_df['sentiment_label'].value_counts().reindex(["Positive", "Neutral", "Negative"], fill_value=0)

plt.figure(figsize=(6, 4))
sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette="viridis")
plt.title("📊 Sentiment Distribution of YouTube Comments")
plt.ylabel("Number of Comments")
plt.xlabel("Sentiment")
plt.tight_layout()
plt.show()

# Print 5 random samples for terminal reference
print("\n🔍 SAMPLE NLP REFERENCES:\n")
sample = processed_df.sample(5, random_state=42)
for i, row in sample.iterrows():
    print(f"🗨️ Original: {row['original']}")
    print(f"🧹 Cleaned: {row['cleaned']}")
    print(f"📚 Lemmas: {row['lemmas']}")
    print(f"🌱 Stems: {row['stems']}")
    print(f"❓ Homonyms: {row['homonyms']}")
    print(f"❤️ Sentiment: {row['sentiment_label']} (Score: {row['sentiment_score']:.2f})\n")
