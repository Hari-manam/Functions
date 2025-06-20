from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from dotenv import load_dotenv
import os

load_dotenv()

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

COLLECTION_NAME = "rag_collection"

# ✅ This must exist at the top level
def upsert_documents(docs):
    points = [
        PointStruct(
            id=idx,
            vector=doc["embedding"],
            payload={"text": doc["text"]}
        )
        for idx, doc in enumerate(docs)
    ]

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )
