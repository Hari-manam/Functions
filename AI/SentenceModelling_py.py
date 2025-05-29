!pip install -q sentence-transformers



import pandas as pd
import json
import io

df = pd.read_json(io.BytesIO(uploaded['News_Category_Dataset_v3.json']), lines=True)
df.head()


import pandas as pd
import io

df = pd.read_json(io.BytesIO(uploaded['News_Category_Dataset_v3.json']), lines=True)
df.head()


df['category'].value_counts().head(10)


from google.colab import files
uploaded = files.upload()


print(label_encoder.classes_)


!pip install -q sentence-transformers


top_categories = ['POLITICS', 'WELLNESS', 'ENTERTAINMENT', 'TRAVEL', 'STYLE & BEAUTY']

# Filter top categories and balance them
df_filtered = df[df['category'].isin(top_categories)]

# Sample 500 per class
balanced_df = df_filtered.groupby('category').apply(lambda x: x.sample(500, random_state=42)).reset_index(drop=True)

print(balanced_df['category'].value_counts())
balanced_df.head()


from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
import numpy as np

# Step 1: Prepare text and labels
sentences = balanced_df['headline'].tolist()
labels = balanced_df['category'].tolist()

# Step 2: Encode text into embeddings
embedder = SentenceTransformer('all-MiniLM-L6-v2')
X = embedder.encode(sentences)

# Step 3: Encode labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(labels)
y_cat = to_categorical(y)

# Step 4: Train ANN model
model = Sequential()
model.add(Input(shape=(X.shape[1],)))
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(len(label_encoder.classes_), activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X, y_cat, epochs=15, batch_size=32, verbose=1)


# User input
user_input = input("📝 Enter a news headline: ")
user_vec = embedder.encode([user_input])

# Predict
prediction = model.predict(user_vec)
predicted_index = np.argmax(prediction)
confidence = prediction[0][predicted_index]
predicted_label = label_encoder.inverse_transform([predicted_index])[0]

# Smart category-based response
category_to_response = {
    "ENTERTAINMENT": "🎬 That sounds like entertainment news!",
    "POLITICS": "🏛️ This seems related to politics.",
    "WELLNESS": "💪 A wellness-related topic, perhaps?",
    "STYLE & BEAUTY": "💅 This is about style or beauty trends.",
    "TRAVEL": "✈️ Sounds like something related to travel!",
}

# Response with threshold
if confidence < 0.6:
    print("😕 I'm not confident about this headline's category.")
else:
    print(f"📊 Predicted Category: {predicted_label} (Confidence: {confidence:.2f})")
    print(f"🤖 Bot: {category_to_response.get(predicted_label, 'I’m still learning about this category.')}")
