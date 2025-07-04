from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

load_dotenv()

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

COLLECTION_NAME = "rag_collection"

def clear_collection():
    client.delete(collection_name=COLLECTION_NAME, points_selector={"filter": {}})

# 1. Create or recreate collection with embedding size 384 (MiniLM size)
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

# 2. Sample documents
docs = [
    "Qdrant is a vector database for storing embeddings.",
    "Flan-T5 is a fine-tuned language model by Google.",
    "Streamlit lets you build web apps with Python easily."
]

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(docs).tolist()

# 3. Upsert into Qdrant
points = [{"id": i, "vector": vec, "payload": {"text": doc}} for i, (doc, vec) in enumerate(zip(docs, embeddings))]
client.upsert(collection_name=COLLECTION_NAME, points=points)

print("✅ Qdrant collection created and sample documents uploaded.")

if __name__ == "__main__":
    clear_collection()
    print(f"Cleared all points in collection: {COLLECTION_NAME}")
