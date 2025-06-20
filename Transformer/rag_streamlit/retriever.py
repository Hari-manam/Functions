
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Filter, SearchRequest
from qdrant_utils import QdrantClient
from dotenv import load_dotenv
import os

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

def retrieve(query, top_k=3):
    query_vector = model.encode(query).tolist()
    results = client.search(
        collection_name="rag_collection",
        query_vector=query_vector,
        limit=top_k
    )
    return [res.payload['text'] for res in results]
