import sys
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
collection = chromadb.PersistentClient(path="chroma_db").get_collection("godot_docs")


def search(question, k=5):
    q = model.encode([question], normalize_embeddings=True).tolist()
    res = collection.query(query_embeddings=q, n_results=k)
    return [
        {"source": m["source"], "chunk_id": m["chunk_id"], "distance": d, "text": t}
        for t, m, d in zip(res["documents"][0], res["metadatas"][0], res["distances"][0])
    ]


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "How do I connect a signal in GDScript?"
    for r in search(question):
        print(f"{r['distance']:.3f}  {r['source']}  (chunk {r['chunk_id']})")
        print(r["text"][:200].replace("\n", " "))
        print()