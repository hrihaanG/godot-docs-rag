import json

from search import search

questions = json.load(open("eval_questions.json", encoding="utf-8"))
rows = []
for q in questions:
    best = search(q["question"], k=1)[0]["distance"]
    rows.append((best, q["id"], q["kind"], q["question"]))

for best, qid, kind, text in sorted(rows):
    print(f"{best:.3f}  #{qid:>2}  {kind:<12} {text[:60]}")