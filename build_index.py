import chromadb
from sentence_transformers import SentenceTransformer
from chunk_docs import chunk_docs
from load_docs import load_docs

model = SentenceTransformer("all-MiniLM-L6-v2")
chunks = chunk_docs(load_docs())

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="godot_docs")

BATCH = 256
for start in range(0, len(chunks), BATCH):
    batch = chunks[start:start + BATCH]
    texts = [c["text"] for c in batch]
    embeddings = model.encode(texts, normalize_embeddings=True).tolist()
    collection.upsert(
        ids=[f"{c['source']}::{c['chunk_id']}" for c in batch],
        documents=texts,
        embeddings=embeddings,
        metadatas=[{"source": c["source"], "chunk_id": c["chunk_id"]} for c in batch],
    )
    print(f"{min(start + BATCH, len(chunks))} / {len(chunks)}")

print("done:", collection.count())