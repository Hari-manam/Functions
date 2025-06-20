from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Qdrant setup
client = QdrantClient(
    url="https://4e4ca221-ef34-46e6-8c8b-a383ce03c643.us-west-1-0.aws.cloud.qdrant.io",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.O00x1JtLK8uqu030wZ9O0_p_tj3AD3eI1e8HQFJePU8"
)

# List all collections
collections = client.get_collections()
print("Available collections:")
for collection in collections.collections:
    print(f"- {collection.name}")

# Get collection info for my-csv-collection
COLLECTION_NAME = "my-csv-collection"
try:
    collection_info = client.get_collection(COLLECTION_NAME)
    print(f"\nCollection info for {COLLECTION_NAME}:")
    print(f"Points count: {collection_info.points_count}")
    print(f"Vectors count: {collection_info.vectors_count}")
except Exception as e:
    print(f"\nError getting collection info: {e}")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Query string
query = "Book a flight"
print(f"\nSearching for: {query}")

# Convert query to vector
query_vector = model.encode(query).tolist()

# Perform similarity search using search (not query_points)
results = client.search(
    collection_name=COLLECTION_NAME,
    query_vector=query_vector,
    limit=3,
    with_payload=True
)

print(f"\nNumber of results found: {len(results)}")

# Display results
for i, hit in enumerate(results, 1):
    print(f"\n{i}. ID: {hit.id}")
    print(f"   Score: {hit.score}")
    print(f"   Payload: {hit.payload}")
