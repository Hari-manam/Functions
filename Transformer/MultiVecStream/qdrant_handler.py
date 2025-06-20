import os
from qdrant_client import QdrantClient as QdrantDBClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
import uuid
from config import get_env_var

QDRANT_URL = get_env_var("QDRANT_URL")
API_KEY = get_env_var("API_KEY")
COLLECTION_NAME = get_env_var("COLLECTION_NAME", "default-collection")

client = QdrantDBClient(url=QDRANT_URL, api_key=API_KEY)

def ensure_collection_exists(dim=512):
    collections = client.get_collections().collections
    if COLLECTION_NAME not in [col.name for col in collections]:
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE)
        )

def upsert_to_qdrant(vector, metadata):
    ensure_collection_exists(dim=len(vector))
    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=vector,
        payload=metadata
    )
    client.upsert(collection_name=COLLECTION_NAME, points=[point])
    print(f"✅ Qdrant: Upserted 1 vector from file: {metadata.get('filename')}")
