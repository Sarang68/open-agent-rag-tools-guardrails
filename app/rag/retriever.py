from typing import List
import chromadb
from sentence_transformers import SentenceTransformer
from app.config import settings

_embedder = SentenceTransformer("all-MiniLM-L6-v2")

def _client():
    return chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)

def get_collection():
    return _client().get_or_create_collection(settings.COLLECTION_NAME)

def add_texts(texts: List[str], metadatas: List[dict], ids: List[str]):
    col = get_collection()
    embeddings = _embedder.encode(texts, normalize_embeddings=True).tolist()
    col.add(documents=texts, metadatas=metadatas, ids=ids, embeddings=embeddings)

def retrieve(query: str, k: int = 4) -> List[dict]:
    col = get_collection()
    q_emb = _embedder.encode([query], normalize_embeddings=True).tolist()
    res = col.query(query_embeddings=q_emb, n_results=k)
    docs = []
    for i in range(len(res["documents"][0])):
        docs.append({
            "text": res["documents"][0][i],
            "metadata": res["metadatas"][0][i],
            "id": res["ids"][0][i],
        })
    return docs

