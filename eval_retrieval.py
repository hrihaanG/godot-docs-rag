import json
from search import search

questions = json.load(open("eval_questions.json", encoding="utf-8"))
normal = [q for q in questions if q["kind"] == "normal"]

KS = (1, 3, 5, 10)
page_hits = {k: 0 for k in KS}
chunk_hits = {k: 0 for k in KS}
results = []

for q in normal:
    found = search(q["question"], k=10)
    page_rank = next(
        (i + 1 for i, h in enumerate(found) if h["source"] in q["expected_sources"]), None
    )
    chunk_rank = next(
        (i + 1 for i, h in enumerate(found)
         if h["source"] in q["expected_sources"]
         and any(kw.lower() in h["text"].lower() for kw in q["keywords"])),
        None,
    )
    for k in KS:
        if page_rank is not None and page_rank <= k:
            page_hits[k] += 1
        if chunk_rank is not None and chunk_rank <= k:
            chunk_hits[k] += 1
    results.append({"id": q["id"], "question": q["question"], "page_rank": page_rank,
                    "chunk_rank": chunk_rank, "top5": [h["source"] for h in found[:5]]})
    print(f"#{q['id']:>2}  page rank: {page_rank or '-':>3}   chunk rank: {chunk_rank or '-':>3}")

print()
for k in KS:
    print(f"hit@{k}: page {page_hits[k]} / {len(normal)}   chunk {chunk_hits[k]} / {len(normal)}")

json.dump(results, open("eval_retrieval_results.json", "w", encoding="utf-8"), indent=2)