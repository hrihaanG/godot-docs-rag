import json
from load_docs import load_docs

docs = {d["source"]: d["text"].lower() for d in load_docs()}
questions = json.load(open("eval_questions.json", encoding="utf-8"))

problems = 0
for q in questions:
    if q["kind"] == "out_of_scope":
        continue
    for src in q["expected_sources"]:
        if src not in docs:
            print(f"#{q['id']}: source not found: {src}")
            problems += 1
    text = " ".join(docs.get(s, "") for s in q["expected_sources"])
    for kw in q["keywords"]:
        if kw.lower() not in text:
            print(f"#{q['id']}: keyword '{kw}' not in the expected pages")
            problems += 1
print(f"{len(questions)} questions checked, {problems} problems")