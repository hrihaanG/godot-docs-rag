import json
from search import search

questions = json.load(open("eval_questions.json", encoding="utf-8"))
normal = [q for q in questions if q["kind"] == "normal"]

KS = (1, 3, 5, 10)
hits_at = {k: 0 for k in KS}
results = []

for q in normal:
    found = search(q["question"], k=10)
    sources = [h["source"] for h in found]
    ranks = [i + 1 for i, s in enumerate(sources) if s in q["expected_sources"]]
    rank = ranks[0] if ranks else None
    for k in KS:
        if rank is not None and rank <= k:
            hits_at[k] += 1
    results.append({"id": q["id"], "question": q["question"], "rank": rank, "top5": sources[:5]})
    print(f"#{q['id']:>2}  rank of expected page: {rank if rank else 'not in top 10'}")

print()
for k in KS:
    print(f"hit@{k}: {hits_at[k]} / {len(normal)}")

print()
print("Misses in top 5:")
for r in results:
    if r["rank"] is None or r["rank"] > 5:
        print(f"#{r['id']} {r['question']}")
        for s in r["top5"]:
            print("   ", s)

json.dump(results, open("eval_retrieval_results.json", "w", encoding="utf-8"), indent=2)