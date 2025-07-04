import os
import time
import hashlib
from qdrant_client import QdrantClient
from dotenv import load_dotenv
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
from embedding_utils import generate_embeddings_from_file
from qdrant_utils import upsert_documents
import pinecone
from pymongo import MongoClient
from pymilvus import connections, Collection
from pinecone import Pinecone

load_dotenv()

WATCH_DIR = "Transformer/rag_streamlit/watch-folder"
print("Current working directory:", os.getcwd())
print("Watching folder:", os.path.abspath(WATCH_DIR))
PROCESSED_DIR = os.path.join(WATCH_DIR, ".processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

active_backends = os.getenv("ACTIVE_BACKENDS", "qdrant,pinecone,mongodb,milvus").split(",")

def get_file_hash(filepath):
    """Generate an MD5 hash of the file content to detect duplicates."""
    hasher = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()
    except Exception as e:
        print(f"❌ Cannot hash file: {filepath} — {e}")
        return None

def already_processed(hash_str):
    return os.path.exists(os.path.join(PROCESSED_DIR, hash_str + ".done"))

def mark_as_processed(hash_str):
    open(os.path.join(PROCESSED_DIR, hash_str + ".done"), "w").close()

def file_exists_pinecone(filename, index):
    # Pinecone does not support direct metadata search, so skip duplicate check for now
    # Optionally, you could maintain a separate mapping or use a workaround for small indexes
    print(f"[Pinecone] Duplicate check for '{filename}' not supported, skipping check.")
    return False

def file_exists_milvus(filename, collection):
    results = collection.query(expr=f'filename == "{filename}"', output_fields=["filename"])
    return len(results) > 0

def upsert_documents_pinecone(chunks):
    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX")
    pc = Pinecone(api_key=api_key)
    index = pc.Index(index_name)
    if not chunks:
        return
    filename = chunks[0].get("filename", None)
    if filename and file_exists_pinecone(filename, index):
        print(f"⚠️ Skipping duplicate file in Pinecone: {filename}")
        return
    vectors = []
    for doc in chunks:
        vectors.append((str(doc["id"]), doc["embedding"], {"text": doc["text"], "filename": doc.get("filename", ""), "chunk_id": doc.get("chunk_id", 0)}))
    if vectors:
        index.upsert(vectors=vectors)
        print(f"✅ Upserted {len(vectors)} vectors into Pinecone.")

def upsert_documents_mongodb(chunks):
    mongodb_uri = os.getenv("MONGODB_ATLAS_URI")
    mongodb_db = os.getenv("MONGODB_ATLAS_DB")
    mongodb_collection = os.getenv("MONGODB_ATLAS_COLLECTION")
    client = MongoClient(mongodb_uri)
    collection = client[mongodb_db][mongodb_collection]
    docs = []
    for doc in chunks:
        docs.append({
            "_id": str(doc["id"]),
            "embedding": doc["embedding"],
            "text": doc["text"],
            "filename": doc.get("filename", ""),
            "chunk_id": doc.get("chunk_id", 0)
        })
    if docs:
        for d in docs:
            try:
                collection.replace_one({"_id": d["_id"]}, d, upsert=True)
            except Exception as e:
                print(f"❌ MongoDB upsert error for {d['_id']}: {e}")
        print(f"✅ Upserted {len(docs)} docs into MongoDB Atlas.")

def upsert_documents_milvus(chunks):
    milvus_uri = os.getenv("MILVUS_URI")
    milvus_api_key = os.getenv("MILVUS_API_KEY")
    milvus_collection = os.getenv("MILVUS_COLLECTION")
    connections.connect(uri=milvus_uri, token=milvus_api_key)
    collection = Collection(milvus_collection)
    if not chunks:
        return
    filename = chunks[0].get("filename", None)
    if filename and file_exists_milvus(filename, collection):
        print(f"⚠️ Skipping duplicate file in Milvus: {filename}")
        return
    primary_keys = []
    vectors = []
    dynamic_fields = []
    for i, doc in enumerate(chunks):
        pk = int(doc.get("chunk_id", i))
        primary_keys.append(pk)
        vectors.append(doc["embedding"])
        dynamic_fields.append({
            "text": doc.get("text", ""),
            "filename": doc.get("filename", ""),
            "chunk_id": doc.get("chunk_id", 0)
        })
    if vectors:
        try:
            collection.insert([primary_keys, vectors], dynamic_fields)
            print(f"✅ Upserted {len(vectors)} vectors into Milvus.")
        except Exception as e:
            print(f"❌ Milvus upsert error: {e}")

def process_file(filepath):
    print(f"\n🔎 Processing file: {filepath}")
    hash_str = get_file_hash(filepath)
    if not hash_str:
        print(f"❌ Skipping file due to hash error: {filepath}")
        return

    is_duplicate = already_processed(hash_str)
    chunks = generate_embeddings_from_file(filepath)
    if not chunks:
        print(f"⚠️ Skipped empty or unsupported file: {filepath}")
        return
    print(f"✅ Extracted {len(chunks)} chunks from {filepath}")

    if "qdrant" in active_backends and not is_duplicate:
        upsert_documents(chunks)  # Qdrant
        print(f"✅ Upserted {filepath} into Qdrant.")
    if "pinecone" in active_backends:
        upsert_documents_pinecone(chunks)
    if "mongodb" in active_backends:
        upsert_documents_mongodb(chunks)
    if "milvus" in active_backends:
        upsert_documents_milvus(chunks)
    if not is_duplicate and "qdrant" in active_backends:
        mark_as_processed(hash_str)

if __name__ == "__main__":
    os.makedirs(WATCH_DIR, exist_ok=True)
    print(f"🔄 Preprocessing existing files in {WATCH_DIR}...")
    for fname in os.listdir(WATCH_DIR):
        fpath = os.path.join(WATCH_DIR, fname)
        if os.path.isfile(fpath):
            process_file(fpath)

    # --- Create a keyword index for the 'filename' field if not present ---
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )
    collection_name = "rag_collection"
    try:
        client.create_payload_index(
            collection_name=collection_name,
            field_name="filename",
            field_schema="keyword"
        )
        print("✅ Created keyword index for 'filename' field.")
    except Exception as e:
        print(f"⚠️ Could not create index for 'filename' (it may already exist): {e}")

    # --- Check if specific files are present in the vector DB ---
    filenames = [
        "Amar Singh v. Union of India, (2011) 7 SCC 69.pdf",
        "Avinash Kumar Chauhan v. Vijay Krishna Mishra, (2009) 2 SCC 532.pdf",
        "B. Ratnamala v. G. Rudramma, 1999 SCC OnLine AP 438.pdf",
        "Bhaskar Laxman Jadhav v. Karamveer Kakasaheb Wagh Education Society, (2013) 11 SCC 531.pdf",
        "CamScanner 05-30-2025 20.34.pdf",
        "eStmt_2025-05-23.pdf",
        "GenAI_Interview_QA (1).docx",
        "Hari.docx",
        "Interplay Between Arbitration Agreements under Arbitration, 1996 & Stamp Act, 1899, In re, (2024) 6 SCC 1.pdf",
        "J_2024_SCC_OnLine_Cal_5386_rishikalyan_gmailcom_20250405_031248_1_13.pdf",
        "J_2024_SCC_OnLine_SC_902_rishikalyan_gmailcom_20250405_032347_1_2.pdf",
        "Manam, Hari Krishna Prasad  -  1170331 NEW STEM OPT I-20 (1).pdf",
        "Rajoli Siva Rami Reddy v. Malepati Subba Rangaiah, 2011 SCC OnLine AP 434.pdf",
        "sample_pdf.pdf",
        "sample_text.txt",
        "Screenshot (253).png",
        "WhatsApp Image 2025-06-09 at 11.02.34 AM.jpeg",
        "WIN_20250417_20_29_51_Pro.jpg"
    ]
    print("\n--- Checking if files are present in the vector DB ---")
    for fname in filenames:
        hits = client.scroll(
            collection_name=collection_name,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="filename",
                        match=MatchValue(value=fname)
                    )
                ]
            ),
            limit=1
        )
        if hits[0]:
            print(f"✅ {fname} is present in the vector DB.")
        else:
            print(f"❌ {fname} is NOT found in the vector DB.")

    # --- Print all unique filenames present in Qdrant DB ---
    # Note: Qdrant's default scroll limit is 10,000 points per call. Increase 'limit' if you have more.
    hits = client.scroll(collection_name=collection_name, limit=1000)
    filenames_in_db = set()
    for point in hits[0]:
        if 'filename' in point.payload:
            filenames_in_db.add(point.payload['filename'])

    print("\n--- Filenames present in Qdrant DB ---")
    for fname in sorted(filenames_in_db):
        print(fname)