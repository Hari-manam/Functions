import os
from config import VECTOR_DB, get_env_var
print("✅ db_router loaded VECTOR_DB =", VECTOR_DB)

vector_db = VECTOR_DB.lower()

# Lazy imports
if vector_db == "qdrant":
    from qdrant_handler import upsert_to_qdrant as db_upsert
elif vector_db == "pinecone":
    from pinecone_client import upsert_to_pinecone as db_upsert
elif vector_db == "weaviate":
    from weaviate_client import upsert_to_weaviate as db_upsert
elif vector_db == "milvus":
    from milvus_client import upsert_to_milvus as db_upsert
elif vector_db == "redis":
    from redis_client import upsert_to_redis as db_upsert
else:
    raise ValueError(f"❌ Unsupported VECTOR_DB: '{vector_db}'")

def route_upsert(vector: list, metadata: dict):
    """
    Routes the given vector and metadata to the appropriate vector DB client.
    """
    print(f"📡 Routing to {vector_db}...")
    return db_upsert(vector, metadata)

# Alias for compatibility with Main.py
upsert_vector = route_upsert
