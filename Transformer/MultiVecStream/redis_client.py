import os
import uuid
import json
import redis
from config import get_env_var

REDIS_HOST = get_env_var("REDIS_HOST")
REDIS_PORT = int(get_env_var("REDIS_PORT", 6379))
REDIS_PASSWORD = get_env_var("REDIS_PASSWORD")
REDIS_INDEX = get_env_var("REDIS_INDEX", "file_vectors")

# Connect to Redis
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True
)

def upsert_to_redis(vector, metadata):
    vector_id = str(uuid.uuid4())
    key = f"{REDIS_INDEX}:{vector_id}"
    data = {
        "embedding": vector,
        "filename": metadata.get("filename", ""),
        "filetype": metadata.get("filetype", "")
    }
    redis_client.set(key, json.dumps(data))
    print(f"✅ Redis: Upserted 1 vector from file: {metadata.get('filename')}")
