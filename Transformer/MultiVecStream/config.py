"""
Configuration file for MultiVecStream vector database settings.
This file contains all the necessary configuration for different vector databases.
"""

import os
from pathlib import Path

# Default vector database
VECTOR_DB = "Qdrant"

# Qdrant Configuration
QDRANT_URL = "https://4e4ca221-ef34-46e6-8c8b-a383ce03c643.us-west-1-0.aws.cloud.qdrant.io"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.O00x1JtLK8uqu030wZ9O0_p_tj3AD3eI1e8HQFJePU8"
COLLECTION_NAME = "my-csv-collection"

# Pinecone Configuration
PINECONE_API_KEY = "pcsk_5iN8EU_Gwa5K7vfTasHKVL6R81ezDLc1idyrnVcWikodA8ocTKRQyWgK8feNC6gnF1sJnn"
PINECONE_ENVIRONMENT = "us-east-1"
PINECONE_INDEX = "multi-db-pipeline"

# Weaviate Configuration
WEAVIATE_URL = "https://i5ex4losowlzqiavfej6g.c0.us-west3.gcp.weaviate.cloud"
WEAVIATE_CLASS = "FileChunk"

# Milvus Configuration
MILVUS_URI = "https://free-01.aws-us-west1.zillizcloud.com"
MILVUS_USER = "db_f134be8b53b853f"
MILVUS_PASSWORD = "Hr7])-^GojT45,Y("
MILVUS_COLLECTION = "file_chunks"

# Redis Configuration
REDIS_HOST = "redis-13723.c84.us-east-1-2.ec2.redns.redis-cloud.com"
REDIS_PORT = 13723
REDIS_PASSWORD = "caEz27aD2LGBkaWYbdUVqXlubBz7S7QF"
REDIS_INDEX = "file_vectors"

def get_env_var(key, default=None):
    """Get environment variable with fallback to config values"""
    return os.getenv(key, globals().get(key, default))

def set_vector_db(db_name):
    """Set the vector database to use"""
    global VECTOR_DB
    VECTOR_DB = db_name 