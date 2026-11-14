import sys

from search import search

question = " ".join(sys.argv[1:])
for h in search(question, 10):
    print(f"{h['distance']:.3f}  {h['source']} (chunk {h['chunk_id']})")