import os
import uuid
import pinecone
from config import get_env_var

PINECONE_API_KEY = get_env_var("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = get_env_var("PINECONE_ENVIRONMENT")
PINECONE_INDEX = get_env_var("PINECONE_INDEX", "default-index")

pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

# Create index if not exists
if PINECONE_INDEX not in pinecone.list_indexes():
    pinecone.create_index(name=PINECONE_INDEX, dimension=512, metric="cosine")

index = pinecone.Index(PINECONE_INDEX)

def upsert_to_pinecone(vector, metadata):
    vector_id = str(uuid.uuid4())
    index.upsert([(vector_id, vector, metadata)])
    print(f"✅ Pinecone: Upserted 1 vector from file: {metadata.get('filename')}")
