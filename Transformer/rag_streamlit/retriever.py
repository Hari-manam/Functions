from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Filter, SearchRequest
from qdrant_utils import QdrantClient
from dotenv import load_dotenv
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from functools import lru_cache
import pinecone
from pymongo import MongoClient
from pymilvus import connections, Collection

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

# Cache loaded models to avoid reloading on every call
@lru_cache(maxsize=4)
def get_model(model_name):
    return SentenceTransformer(model_name)

def retrieve(query, top_k=8, embedding_model="all-MiniLM-L6-v2"):
    """
    Standard RAG: Always return top_k most similar chunks, no similarity threshold. Print similarity scores for debugging.
    """
    model = get_model(embedding_model)
    query_vector = model.encode(query).reshape(1, -1)
    results = client.search(
        collection_name="rag_collection",
        query_vector=query_vector.tolist()[0],
        limit=top_k
    )
    print(f"Qdrant returned {len(results)} results for query: '{query}'")
    for res in results:
        if hasattr(res, 'vector') and res.vector is not None:
            chunk_vector = np.array(res.vector).reshape(1, -1)
            sim = cosine_similarity(query_vector, chunk_vector)[0][0]
            print(f"[Standard RAG] Chunk: {res.payload['text'][:80]}... | Similarity: {sim:.2f}")
    return [res.payload for res in results]

def fusion_retrieve(query, top_k=8, embedding_model="all-MiniLM-L6-v2"):
    """
    Fusion RAG: Retrieve top_k results for the original query and a rephrased query, then combine and deduplicate.
    """
    model = get_model(embedding_model)
    # Original query
    query_vector = model.encode(query).reshape(1, -1)
    results1 = client.search(
        collection_name="rag_collection",
        query_vector=query_vector.tolist()[0],
        limit=top_k
    )
    # Rephrased query (add 'explain' to the end)
    rephrased_query = query + " explain"
    rephrased_vector = model.encode(rephrased_query).reshape(1, -1)
    results2 = client.search(
        collection_name="rag_collection",
        query_vector=rephrased_vector.tolist()[0],
        limit=top_k
    )
    # Combine and deduplicate by (filename, chunk_id) or text
    seen = set()
    fused = []
    for res in list(results1) + list(results2):
        payload = res.payload
        key = (payload.get('filename'), payload.get('chunk_id'))
        if key not in seen:
            fused.append(payload)
            seen.add(key)
    print(f"Fusion RAG: returning {len(fused)} unique chunks for query: '{query}'")
    return fused

def speculative_retrieve(query, top_k=8, embedding_model="all-MiniLM-L6-v2"):
    """
    Speculative RAG: Generate several query variants, retrieve top_k for each, and fuse/deduplicate the results.
    """
    model = get_model(embedding_model)
    query_variants = [
        query,
        query + " explain",
        query + " summary",
        query + " key points",
        "What are the main points about: " + query,
    ]
    all_results = []
    for variant in query_variants:
        q_vec = model.encode(variant).reshape(1, -1)
        results = client.search(
            collection_name="rag_collection",
            query_vector=q_vec.tolist()[0],
            limit=top_k
        )
        all_results.extend(results)
    # Deduplicate by (filename, chunk_id)
    seen = set()
    fused = []
    for res in all_results:
        payload = res.payload
        key = (payload.get('filename'), payload.get('chunk_id'))
        if key not in seen:
            fused.append(payload)
            seen.add(key)
    print(f"Speculative RAG: returning {len(fused)} unique chunks for query: '{query}'")
    return fused

def corrective_retrieve(query, top_k=8, similarity_threshold=0.01, embedding_model="all-MiniLM-L6-v2"):
    """
    Corrective RAG: Retrieve top_k, filter by similarity threshold (default 0.01). Print similarity scores for debugging.
    """
    model = get_model(embedding_model)
    query_vector = model.encode(query).reshape(1, -1)
    results = client.search(
        collection_name="rag_collection",
        query_vector=query_vector.tolist()[0],
        limit=top_k
    )
    filtered = []
    for res in results:
        if hasattr(res, 'vector') and res.vector is not None:
            chunk_vector = np.array(res.vector).reshape(1, -1)
            sim = cosine_similarity(query_vector, chunk_vector)[0][0]
            print(f"[Corrective RAG] Chunk: {res.payload['text'][:80]}... | Similarity: {sim:.2f}")
            if sim >= similarity_threshold:
                filtered.append(res.payload)
    print(f"Corrective RAG: returning {len(filtered)} chunks above threshold {similarity_threshold} for query: '{query}'")
    return filtered

def agentic_retrieve(query, top_k=8, embedding_model="all-MiniLM-L6-v2"):
    """
    Agentic RAG: Retrieve top_k, then select diverse chunks (simulate agentic behavior by picking most dissimilar among top results).
    """
    model = get_model(embedding_model)
    query_vector = model.encode(query).reshape(1, -1)
    results = client.search(
        collection_name="rag_collection",
        query_vector=query_vector.tolist()[0],
        limit=top_k*2  # get more to allow diversity
    )
    # Select the most dissimilar chunks among the top results (simple diversity)
    selected = []
    used = set()
    for res in results:
        payload = res.payload
        key = (payload.get('filename'), payload.get('chunk_id'))
        if key in used:
            continue
        if not selected:
            selected.append(payload)
            used.add(key)
        else:
            # Only add if not too similar to already selected
            chunk_vector = np.array(res.vector).reshape(1, -1)
            is_diverse = all(cosine_similarity(chunk_vector, np.array([r['embedding']]))[0][0] < 0.7 for r in selected if 'embedding' in r)
            if is_diverse:
                selected.append(payload)
                used.add(key)
        if len(selected) >= top_k:
            break
    print(f"Agentic RAG: returning {len(selected)} diverse chunks for query: '{query}'")
    return selected

def expanded_corrective_retrieve(query, top_k=8, similarity_threshold=0.01, embedding_model="all-MiniLM-L6-v2"):
    """
    Expanded Corrective RAG: For each of several query variants, retrieve top_k, filter by similarity threshold, and fuse/deduplicate the results.
    """
    model = get_model(embedding_model)
    query_variants = [
        query,
        query + " explain",
        query + " summary",
        query + " key points",
        "What are the main points about: " + query,
    ]
    all_results = []
    for variant in query_variants:
        q_vec = model.encode(variant).reshape(1, -1)
        results = client.search(
            collection_name="rag_collection",
            query_vector=q_vec.tolist()[0],
            limit=top_k
        )
        for res in results:
            if hasattr(res, 'vector') and res.vector is not None:
                chunk_vector = np.array(res.vector).reshape(1, -1)
                sim = cosine_similarity(q_vec, chunk_vector)[0][0]
                print(f"[Expanded Corrective RAG] Query: '{variant}' | Chunk: {res.payload['text'][:80]}... | Similarity: {sim:.2f}")
                if sim >= similarity_threshold:
                    all_results.append((sim, res.payload))
    # Deduplicate by (filename, chunk_id)
    seen = set()
    fused = []
    # Sort by similarity descending
    all_results.sort(reverse=True, key=lambda x: x[0])
    for sim, payload in all_results:
        key = (payload.get('filename'), payload.get('chunk_id'))
        if key not in seen:
            fused.append(payload)
            seen.add(key)
    print(f"Expanded Corrective RAG: returning {len(fused)} unique chunks above threshold {similarity_threshold} for query: '{query}'")
    return fused

def qdrant_retrieve(query, top_k=8, embedding_model="all-MiniLM-L6-v2"):
    # Use your existing retrieve function for Qdrant
    return retrieve(query, top_k=top_k, embedding_model=embedding_model)

# Pinecone retriever

def pinecone_retrieve(query, top_k=8, embedding_model="all-MiniLM-L6-v2"):
    api_key = os.getenv("PINECONE_API_KEY")
    env = os.getenv("PINECONE_ENV")
    index_name = os.getenv("PINECONE_INDEX")
    pinecone.init(api_key=api_key, environment=env)
    index = pinecone.Index(index_name)
    model = get_model(embedding_model)
    query_vector = model.encode(query).tolist()
    res = index.query(vector=query_vector, top_k=top_k, include_metadata=True)
    results = []
    for match in res["matches"]:
        results.append({
            "text": match["metadata"].get("text", ""),
            "score": match["score"],
            "filename": match["metadata"].get("filename", ""),
            "source": "pinecone"
        })
    return results

# MongoDB Atlas retriever

def mongodb_retrieve(query, top_k=8, embedding_model="all-MiniLM-L6-v2"):
    mongodb_uri = os.getenv("MONGODB_ATLAS_URI")
    mongodb_db = os.getenv("MONGODB_ATLAS_DB")
    mongodb_collection = os.getenv("MONGODB_ATLAS_COLLECTION")
    mongodb_index = os.getenv("MONGODB_ATLAS_VECTOR_INDEX")
    client = MongoClient(mongodb_uri)
    collection = client[mongodb_db][mongodb_collection]
    model = get_model(embedding_model)
    query_vector = model.encode(query).tolist()
    pipeline = [
        {
            "$vectorSearch": {
                "index": mongodb_index,
                "queryVector": query_vector,
                "path": "embedding",
                "numCandidates": 100,
                "limit": top_k
            }
        }
    ]
    results = []
    for doc in collection.aggregate(pipeline):
        results.append({
            "text": doc.get("text", ""),
            "score": doc.get("score", 0),
            "filename": doc.get("filename", ""),
            "source": "mongodb"
        })
    return results

# Milvus retriever

def milvus_retrieve(query, top_k=8, embedding_model="all-MiniLM-L6-v2"):
    milvus_uri = os.getenv("MILVUS_URI")
    milvus_api_key = os.getenv("MILVUS_API_KEY")
    milvus_collection = os.getenv("MILVUS_COLLECTION")
    connections.connect(uri=milvus_uri, token=milvus_api_key)
    collection = Collection(milvus_collection)
    model = get_model(embedding_model)
    query_vector = model.encode(query).tolist()
    search_params = {"metric_type": "IP", "params": {"nprobe": 10}}
    res = collection.search(
        data=[query_vector],
        anns_field="embedding",
        param=search_params,
        limit=top_k,
        output_fields=["text", "filename"]
    )
    results = []
    for hits in res:
        for hit in hits:
            results.append({
                "text": hit.entity.get("text", ""),
                "score": hit.distance,
                "filename": hit.entity.get("filename", ""),
                "source": "milvus"
            })
    return results

# Unified retriever that queries selected backends and merges results
def unified_retrieve(query, top_k=8, embedding_model="all-MiniLM-L6-v2", backends=["qdrant"]):
    results = []
    if "qdrant" in backends:
        qdrant_results = qdrant_retrieve(query, top_k, embedding_model)
        for doc in qdrant_results:
            doc["source"] = "qdrant"
        results += qdrant_results
    if "pinecone" in backends:
        pinecone_results = pinecone_retrieve(query, top_k, embedding_model)
        for doc in pinecone_results:
            doc["source"] = "pinecone"
        results += pinecone_results
    if "mongodb" in backends:
        mongodb_results = mongodb_retrieve(query, top_k, embedding_model)
        for doc in mongodb_results:
            doc["source"] = "mongodb"
        results += mongodb_results
    if "milvus" in backends:
        milvus_results = milvus_retrieve(query, top_k, embedding_model)
        for doc in milvus_results:
            doc["source"] = "milvus"
        results += milvus_results
    # Optionally deduplicate and rerank here
    return results[:top_k]
