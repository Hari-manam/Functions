from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

COLLECTION_NAME = "rag_collection"

# ✅ This must exist at the top level
def upsert_documents(docs):
    points = []
    for doc in docs:
        # Use a UUID for each chunk as required by Qdrant
        unique_id = str(uuid.uuid4())
        print(f"Upserting chunk ID: {unique_id} (file: {doc.get('filename')})")
        points.append(
            PointStruct(
                id=unique_id,
                vector=doc["embedding"],
                payload={
                    "text": doc["text"],
                    "filename": doc.get("filename"),
                    "chunk_id": doc.get("chunk_id")
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )
