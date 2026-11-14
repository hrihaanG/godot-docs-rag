from search import search

ON_TOPIC = [
    "your question 1",
    "your question 2",
    "your question 3",
    "your question 4",
    "your question 5",
]
OFF_TOPIC = [
    "your question 1",
    "your question 2",
    "your question 3",
    "your question 4",
    "your question 5",
]

for label, questions in (("on-topic", ON_TOPIC), ("off-topic", OFF_TOPIC)):
    for q in questions:
        best = search(q, k=1)[0]["distance"]
        print(f"{best:.3f}  {label:<9} {q[:70]}")