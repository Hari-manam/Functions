import os
import time
import mimetypes
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import pdfplumber
import pandas as pd
from PIL import Image
from docx import Document
from pathlib import Path

# Import config
from config import set_vector_db, VECTOR_DB

# 👉 Prompt for vector DB selection
print("👉 Enter the number of the vector DB to use:")
print("1. Qdrant\n2. Pinecone\n3. Weaviate\n4. Milvus\n5. Redis")
choice = input("Your choice (1-5): ").strip()

db_map = {
    "1": "Qdrant",
    "2": "Pinecone",
    "3": "Weaviate",
    "4": "Milvus",
    "5": "Redis"
}
selected_db = db_map.get(choice, "Qdrant")

# 🔄 Update config dynamically
set_vector_db(selected_db)
print("✅ VECTOR_DB set to:", selected_db)

# ⏳ Only now import upsert_vector
from db_router import upsert_vector

# Load SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")

# Ensure 512-dim output
def resize_vector(vec, target_dim=512):
    vec = np.array(vec)
    if len(vec) < target_dim:
        padded = np.pad(vec, (0, target_dim - len(vec)))
    else:
        padded = vec[:target_dim]
    return padded.tolist()

# File Handler
class FileProcessor(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory or event.src_path.endswith("~"):
            return
        self.process(event.src_path)

    def on_created(self, event):
        if event.is_directory or event.src_path.endswith("~"):
            return
        self.process(event.src_path)

    def process(self, path):
        try:
            filename = os.path.basename(path)
            ext = os.path.splitext(path)[-1].lower()

            if ext in [".csv", ".xlsx"]:
                df = pd.read_csv(path) if ext == ".csv" else pd.read_excel(path)
                for _, row in df.iterrows():
                    text = " ".join(str(cell) for cell in row if pd.notnull(cell))
                    vector = model.encode(text)
                    final_vector = resize_vector(vector)
                    upsert_vector(final_vector, {"filename": filename, "filetype": ext})

            elif ext == ".pdf":
                with pdfplumber.open(path) as pdf:
                    text = "\n".join([page.extract_text() or "" for page in pdf.pages])
                vector = model.encode(text)
                final_vector = resize_vector(vector)
                upsert_vector(final_vector, {"filename": filename, "filetype": ext})

            elif ext == ".docx":
                try:
                    doc = Document(path)
                    text = "\n".join([p.text for p in doc.paragraphs])
                    vector = model.encode(text)
                    final_vector = resize_vector(vector)
                    upsert_vector(final_vector, {"filename": filename, "filetype": ext})
                except Exception:
                    print(f"⚠️ Locked or OneDrive docx file: {filename}")

            elif ext in [".png", ".jpg", ".jpeg"]:
                image = Image.open(path).convert("RGB")
                image = image.resize((224, 224))
                pixels = np.array(image).flatten()
                vec = pixels[:512] if len(pixels) >= 512 else np.pad(pixels, (0, 512 - len(pixels)))
                upsert_vector(vec.tolist(), {"filename": filename, "filetype": ext})

            elif ext in [".txt", ".xml"]:
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()
                vector = model.encode(text)
                final_vector = resize_vector(vector)
                upsert_vector(final_vector, {"filename": filename, "filetype": ext})

            else:
                print(f"⚠️ Unsupported file type: {filename}")

        except Exception as e:
            print(f"❌ Error processing {path}: {e}")

# Watch folder
if __name__ == "__main__":
    watch_path = os.path.join(os.path.dirname(__file__), "watch-folder")
    if not os.path.exists(watch_path):
        os.makedirs(watch_path)

    print(f"📂 Watching: {watch_path}")
    observer = Observer()
    observer.schedule(FileProcessor(), watch_path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
