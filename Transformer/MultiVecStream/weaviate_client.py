import os
import uuid
import weaviate
from config import get_env_var

WEAVIATE_URL = get_env_var("WEAVIATE_URL")
WEAVIATE_CLASS = get_env_var("WEAVIATE_CLASS", "FileChunk")

# Create client
client = weaviate.Client(
    url=WEAVIATE_URL,
    additional_headers={"X-OpenAI-Api-Key": "no-key-required-on-sandbox"}
)

def ensure_class_exists(dim=512):
    if not client.schema.contains({"classes": [{"class": WEAVIATE_CLASS}]}):
        schema = {
            "class": WEAVIATE_CLASS,
            "vectorizer": "none",
            "vectorIndexConfig": {"distance": "cosine"},
            "properties": [
                {"name": "filename", "dataType": ["text"]},
                {"name": "filetype", "dataType": ["text"]}
            ]
        }
        client.schema.create_class(schema)

def upsert_to_weaviate(vector, metadata):
    ensure_class_exists(dim=len(vector))
    client.data_object.create(
        data_object={
            "filename": metadata.get("filename", ""),
            "filetype": metadata.get("filetype", "")
        },
        class_name=WEAVIATE_CLASS,
        vector=vector,
        uuid=str(uuid.uuid4())
    )
    print(f"✅ Weaviate: Upserted 1 vector from file: {metadata.get('filename')}")
