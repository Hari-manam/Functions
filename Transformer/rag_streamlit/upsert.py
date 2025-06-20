import os
import time
import hashlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from embedding_utils import generate_embeddings_from_file
from qdrant_utils import upsert_documents

WATCH_DIR = "watch-folder"
PROCESSED_DIR = os.path.join(WATCH_DIR, ".processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

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

def process_file(filepath):
    hash_str = get_file_hash(filepath)
    if not hash_str:
        return

    if already_processed(hash_str):
        print(f"⚠️ Skipping duplicate file: {filepath}")
        return

    try:
        chunks = generate_embeddings_from_file(filepath)
        if not chunks:
            print(f"⚠️ Skipped empty or unsupported file: {filepath}")
            return
        upsert_documents(chunks)
        mark_as_processed(hash_str)
        print(f"✅ Embedded & upserted: {filepath}")
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")

class WatchHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            process_file(event.src_path)

if __name__ == "__main__":
    os.makedirs(WATCH_DIR, exist_ok=True)

    print(f"🔄 Preprocessing existing files in {WATCH_DIR}...")
    for fname in os.listdir(WATCH_DIR):
        fpath = os.path.join(WATCH_DIR, fname)
        if os.path.isfile(fpath):
            process_file(fpath)

    print(f"📂 Watching: {WATCH_DIR}")
    event_handler = WatchHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
