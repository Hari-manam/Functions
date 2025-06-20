import os
import pdfplumber
import docx
import pandas as pd
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

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
            # Placeholder text for image files
            text = f"This is an image file: {os.path.basename(file_path)}"
        else:
            print(f"⚠️ Unsupported file type: {ext}")
            return []

        chunks = split_text(text)
        embeddings = model.encode(chunks).tolist()

        return [
            {"id": f"{os.path.basename(file_path)}_{i}", "text": chunk, "embedding": embedding}
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

def split_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks
