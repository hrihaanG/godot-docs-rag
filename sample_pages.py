import random
from load_docs import load_docs

docs = [d for d in load_docs() if len(d["text"]) > 3000]
random.Random(42).shuffle(docs)
for d in docs[:12]:
    body = "\n".join(
        line for line in d["text"].splitlines()
        if line.strip() and not line.startswith("..")
    )
    print("=" * 70)
    print(d["source"])
    print(body[:700])