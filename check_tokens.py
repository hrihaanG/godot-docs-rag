from sentence_transformers import SentenceTransformer
from chunk_docs import chunk_docs
from load_docs import load_docs

model = SentenceTransformer("all-MiniLM-L6-v2")
chunks = chunk_docs(load_docs())
counts = [len(model.tokenizer.encode(c["text"])) for c in chunks]
limit = model.max_seq_length
over = sum(1 for n in counts if n > limit)
print(f"{over} of {len(chunks)} chunks exceed {limit} tokens")
print("longest:", max(counts), "tokens")
print("average:", sum(counts) // len(counts), "tokens")