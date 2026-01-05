import os
import uuid
from pypdf import PdfReader
from app.rag.retriever import add_texts

def chunk_text(text: str, chunk_size: int = 900, overlap: int = 150):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = max(0, end - overlap)
    return [c.strip() for c in chunks if c.strip()]

def ingest_pdf(pdf_path: str):
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        full_text += (page.extract_text() or "") + "\n"

    chunks = chunk_text(full_text)
    ids = [str(uuid.uuid4()) for _ in chunks]
    metadatas = [{"source": os.path.basename(pdf_path)} for _ in chunks]
    add_texts(chunks, metadatas, ids)
    return len(chunks)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python -m app.rag.ingest <path-to-pdf>")
    count = ingest_pdf(sys.argv[1])
    print(f"Ingested {count} chunks.")

