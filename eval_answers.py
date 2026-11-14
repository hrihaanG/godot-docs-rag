import json
import re
import sys
import time

from answer import answer

questions = json.load(open("eval_questions.json", encoding="utf-8"))
only = {int(a) for a in sys.argv[1:]}
if only:
    questions = [q for q in questions if q["id"] in only]
REFUSALS = ("could not find", "couldn't find", "cannot find", "can't find")


def ask(question):
    for _ in range(3):
        try:
            return answer(question)
        except Exception as e:
            print(f"   {type(e).__name__}: {str(e)[:200]} - waiting 30s")
            time.sleep(30)
    return None, []


def cited_numbers(text):
    nums = []
    for group in re.findall(r"\[(\d+(?:\s*,\s*\d+)*)\]", text):
        nums += [int(n) for n in group.split(",")]
    return nums


results = []
for q in questions:
    text, hits = ask(q["question"])
    r = {"id": q["id"], "kind": q["kind"], "question": q["question"],
         "answer": text, "sources": [h["source"] for h in hits], "passed": False}
    if text is not None:
        low = text.lower()
        refused = any(p in low for p in REFUSALS)
        nums = cited_numbers(text)
        if q["kind"] == "out_of_scope":
            r["passed"] = refused
        else:
            r["retrieved"] = any(s in q["expected_sources"] for s in r["sources"])
            r["keywords"] = all(k.lower() in low for k in q["keywords"])
            r["cites_expected"] = any(
                1 <= n <= len(hits) and r["sources"][n - 1] in q["expected_sources"]
                for n in nums
            )
            r["valid_numbers"] = all(1 <= n <= len(hits) for n in nums)
            r["passed"] = (not refused and r["keywords"]
                           and r["cites_expected"] and r["valid_numbers"])
    results.append(r)
    print(f"#{q['id']:>2}  {'PASS' if r['passed'] else 'FAIL'}")
    time.sleep(6)

normal = [r for r in results if r["kind"] == "normal"]
oos = [r for r in results if r["kind"] == "out_of_scope"]
print()
print(f"normal questions passed: {sum(r['passed'] for r in normal)} / {len(normal)}")
print(f"out-of-scope refused:    {sum(r['passed'] for r in oos)} / {len(oos)}")

print()
print("Failures (review these by hand):")
for r in [r for r in normal if not r["passed"]]:
    print(f"#{r['id']} {r['question']}")
    print("   retrieved:", r.get("retrieved"), "| keywords:", r.get("keywords"),
          "| cites expected:", r.get("cites_expected"))
    print("   answer:", (r["answer"] or "NO ANSWER")[:300].replace("\n", " "))

out = "eval_answer_results_partial.json" if only else "eval_answer_results.json"
json.dump(results, open(out, "w", encoding="utf-8"), indent=2)