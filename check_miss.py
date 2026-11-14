import sys
from load_docs import load_docs

path, word = sys.argv[1], sys.argv[2].lower()
doc = next(d for d in load_docs() if d["source"] == path)
for line in doc["text"].splitlines():
    if word in line.lower():
        print(line.strip())