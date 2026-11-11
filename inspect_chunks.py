from chunk_docs import chunk_docs
from load_docs import load_docs

chunks = chunk_docs(load_docs())
big = sorted(chunks, key=lambda c: len(c["text"]), reverse=True)[:5]
for c in big:
    print(len(c["text"]), c["source"], c["chunk_id"])
print()
print(big[0]["text"][:300])
print("...")
print(sum(1 for c in chunks if len(c["text"]) > 2000), "chunks over 2000 chars")