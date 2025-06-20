# debug_qdrant.py
import os
from qdrant_client import QdrantClient

url = os.getenv("QDRANT_URL")
api_key = os.getenv("QDRANT_API_KEY")

print("🧪 QDRANT_URL =", url)
print("🔐 QDRANT_API_KEY is set?", api_key is not None)

client = QdrantClient(url=url, api_key=api_key)

# Optional: Check collections
collections = client.get_collections()
print("📦 Collections:", collections)

# Optional: Check vector size
info = client.get_collection("rag_collection")
print("📏 Vector size in Qdrant:", info.vector_size)
