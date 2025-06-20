from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType
import os
import uuid
from config import get_env_var

connections.connect(
    uri=get_env_var("MILVUS_URI"),
    user=get_env_var("MILVUS_USER"),
    password=get_env_var("MILVUS_PASSWORD")
)

collection_name = get_env_var("MILVUS_COLLECTION")

fields = [
    FieldSchema(name="primary_key", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=512),
]
schema = CollectionSchema(fields, description="Auto-created collection for 512D file vectors")

if collection_name not in [col.name for col in Collection.list()]:
    collection = Collection(name=collection_name, schema=schema)
    print(f"✅ Created collection: {collection_name}")
else:
    collection = Collection(name=collection_name)
    print(f"✅ Collection already exists: {collection_name}")

def upsert_to_milvus(vector, metadata):
    """
    Upsert a vector and metadata to Milvus collection.
    """
    # Load the collection
    collection = Collection(name=collection_name)
    collection.load()
    
    # Prepare data for insertion
    data = [vector]
    
    # Insert the vector
    collection.insert(data)
    collection.flush()
    
    print(f"✅ Milvus: Upserted 1 vector from file: {metadata.get('filename')}")
