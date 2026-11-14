from search import search

hits = search("How do I make a character jump in 2D?")
for n in (1, 4):
    h = hits[n - 1]
    print(f"--- [{n}] {h['source']} (chunk {h['chunk_id']})")
    print(h["text"])
    print("contains 'down':", "down" in h["text"].lower())
    print("contains '-400':", "-400" in h["text"])
    print()