import os
import time
import mimetypes
import math
import msvcrt
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from PIL import Image
import pdfplumber
import requests
from docx import Document

# Qdrant Configuration
QDRANT_URL = "https://4e4ca221-ef34-46e6-8c8b-a383ce03c643.us-west-1-0.aws.cloud.qdrant.io"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.O00x1JtLK8uqu030wZ9O0_p_tj3AD3eI1e8HQFJePU8"
COLLECTION_NAME = "my-csv-collection"

# Load model
model = SentenceTransformer("clip-ViT-B-32")
text_model = model
image_model = model

# Validate embedding size
assert len(text_model.encode(["test"])[0]) == 512
assert len(image_model.encode(["test"])[0]) == 512

# Init Qdrant client
client = QdrantClient(url=QDRANT_URL, api_key=API_KEY, timeout=60)
if not client.collection_exists(COLLECTION_NAME):
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=512, distance=Distance.COSINE)
    )

def generate_text_from_dataframe(df):
    return [", ".join([f"{col}: {row[col]}" for col in df.columns if pd.notnull(row[col])]) for _, row in df.iterrows()]

def process_csv_or_excel(file_path):
    print(f"\n📊 Detected table file: {file_path}")
    try:
        mime, _ = mimetypes.guess_type(file_path)
        df = pd.read_csv(file_path) if file_path.endswith(".csv") or (mime and "csv" in mime) else pd.read_excel(file_path)
        if df.empty:
            print(f"⚠️ File {file_path} is empty.")
            return
        print(f"📄 Loaded DataFrame: {len(df)} rows, {len(df.columns)} columns")
        texts = generate_text_from_dataframe(df)
        start_id = int(time.time() * 1000)
        ids = list(range(start_id, start_id + len(texts)))
        vectors = text_model.encode(texts)
        points = [
            PointStruct(id=idx, vector=vec.tolist(), payload={"summary": text, "type": "table", "source_file": os.path.basename(file_path)})
            for idx, vec, text in zip(ids, vectors, texts)
        ]
        for i in range(0, len(points), 100):
            batch = points[i:i + 100]
            try:
                client.upsert(collection_name=COLLECTION_NAME, points=batch)
                print(f"📤 Upserted batch {i//100 + 1} of {math.ceil(len(points)/100)}")
            except requests.exceptions.RequestException:
                print(f"⚠️ Retry batch {i//100 + 1} after network error")
                time.sleep(2)
                client.upsert(collection_name=COLLECTION_NAME, points=batch)
        time.sleep(0.5)
    except Exception as e:
        print(f"❌ CSV/XLS processing failed for {file_path}: {e}")

def process_pdf(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages).strip()
    except Exception as e:
        print(f"❌ Error reading PDF {file_path}: {e}")
        return None

def process_txt_or_xml(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        print(f"❌ Error reading text file {file_path}: {e}")
        return None

def wait_until_unlocked(file_path, timeout=20):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with open(file_path, 'r+b') as f:
                msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
                return True
        except:
            time.sleep(1)
    return False

def process_docx(file_path, retries=10, delay=2):
    for attempt in range(1, retries + 1):
        try:
            if not os.path.exists(file_path):
                print(f"⏳ DOCX file not found yet, retrying... ({attempt}/{retries})")
                time.sleep(delay)
                continue
            if not wait_until_unlocked(file_path):
                print(f"⏳ DOCX still locked, retrying... ({attempt}/{retries})")
                time.sleep(delay)
                continue
            doc = Document(file_path)
            full_text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
            if full_text.strip():
                return full_text.strip()
            else:
                print(f"⏳ DOCX is empty or not ready, retrying... ({attempt}/{retries})")
                time.sleep(delay)
        except Exception as e:
            print(f"⏳ DOCX not ready, retrying... ({attempt}/{retries}) - {e}")
            time.sleep(delay)
    print(f"❌ Failed to read DOCX after {retries} attempts: {file_path}")
    return None

def process_image(file_path):
    try:
        img = Image.open(file_path)
        return image_model.encode([img])[0]
    except Exception as e:
        print(f"❌ Error reading image file {file_path}: {e}")
        return None

def upsert_file_to_qdrant(file_path):
    if os.path.basename(file_path).startswith("~$"):
        print(f"⏭️ Skipping temp file: {file_path}")
        return

    ext = os.path.splitext(file_path)[1].lower()
    point_id = int(time.time() * 1000)
    payload = {"source_file": os.path.basename(file_path)}

    try:
        if ext in [".csv", ".xls", ".xlsx"]:
            process_csv_or_excel(file_path)
            return
        elif ext == ".docx":
            text = process_docx(file_path)
            if not text:
                return
            vector = text_model.encode([text])[0]
            payload["type"] = "docx"
        elif ext == ".pdf":
            text = process_pdf(file_path)
            if not text:
                return
            vector = text_model.encode([text])[0]
            payload["type"] = "pdf"
        elif ext in [".txt", ".xml"]:
            text = process_txt_or_xml(file_path)
            if not text:
                return
            vector = text_model.encode([text])[0]
            payload["type"] = ext[1:]
        elif ext in [".jpg", ".jpeg", ".png", ".bmp", ".gif"]:
            vector = process_image(file_path)
            if vector is None:
                return
            payload["type"] = "image"
        else:
            print(f"⚠️ Unsupported file type: {file_path}")
            return

        client.upsert(collection_name=COLLECTION_NAME, points=[
            PointStruct(id=point_id, vector=vector.tolist(), payload=payload)
        ])
        print(f"✅ Upserted 1 vector from {file_path}")
    except Exception as e:
        print(f"❌ Error processing file {file_path}: {e}")

class FileWatcher(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f"🆕 File created or updated: {event.src_path}")
            upsert_file_to_qdrant(event.src_path)
    def on_created(self, event):
        if not event.is_directory:
            print(f"🆕 New file created: {event.src_path}")
            upsert_file_to_qdrant(event.src_path)

if __name__ == "__main__":
    folder_path = os.path.join(os.path.dirname(__file__), "watch-folder")
    os.makedirs(folder_path, exist_ok=True)
    event_handler = FileWatcher()
    observer = Observer()
    observer.schedule(event_handler, path=folder_path, recursive=False)
    observer.start()
    print(f"\n📂 Watching: {folder_path}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
