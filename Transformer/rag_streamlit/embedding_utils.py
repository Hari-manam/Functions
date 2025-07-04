import os
import pdfplumber
import docx
import pandas as pd
from sentence_transformers import SentenceTransformer

# Use 384-dim model for Qdrant compatibility
model = SentenceTransformer("all-MiniLM-L6-v2")  # 384-dim
# model = SentenceTransformer("paraphrase-MiniLM-L6-v2")  # also 384-dim
# model = SentenceTransformer("nlpaueb/legal-bert-base-uncased")  # 768-dim (do NOT use for 384-dim Qdrant)

def generate_embeddings_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == ".pdf":
            text = extract_text_from_pdf(file_path)
        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        elif ext == ".csv":
            df = pd.read_csv(file_path)
            text = df.astype(str).apply(" ".join, axis=1).str.cat(sep=" ")
        elif ext == ".docx":
            doc = docx.Document(file_path)
            text = "\n".join([p.text for p in doc.paragraphs])
        elif ext in [".xls", ".xlsx"]:
            df = pd.read_excel(file_path)
            text = df.astype(str).apply(" ".join, axis=1).str.cat(sep=" ")
        elif ext in [".jpg", ".jpeg", ".png"]:
            text = f"This is an image file: {os.path.basename(file_path)}"
        else:
            print(f"⚠️ Unsupported file type: {ext}")
            return []

        # Use improved chunking for legal documents
        chunks = split_text(text, chunk_size=1000, overlap=250)
        embeddings = model.encode(chunks).tolist()

        return [
            {"id": f"{os.path.basename(file_path)}_{i}",
             "text": chunk,
             "embedding": embedding,
             "filename": os.path.basename(file_path),
             "chunk_id": i
            }
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings))
        ]
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return []

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def split_text(text, chunk_size=1000, overlap=250):
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    chunks = []
    current_chunk = []
    current_length = 0
    for para in paragraphs:
        para_len = len(para.split())
        if current_length + para_len > chunk_size and current_chunk:
            chunks.append(' '.join(current_chunk))
            # Overlap logic: keep last 'overlap' words for next chunk
            if overlap > 0 and len(current_chunk) > 0:
                overlap_words = ' '.join(current_chunk).split()[-overlap:]
                current_chunk = [' '.join(overlap_words)]
                current_length = len(overlap_words)
            else:
                current_chunk = []
                current_length = 0
        current_chunk.append(para)
        current_length += para_len
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks
