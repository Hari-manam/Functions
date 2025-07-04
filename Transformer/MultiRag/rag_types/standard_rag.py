from qdrant_client import QdrantClient

client = QdrantClient("localhost", port=6333)  # Adjust host/port as needed

def retrieve_docs(query):
    # Example: search in Qdrant collection
    search_result = client.search(
        collection_name="your_collection",
        query_vector=[...],  # You need to embed your query to a vector
        limit=5
    )
    docs = [hit.payload["text"] for hit in search_result]
    return docs