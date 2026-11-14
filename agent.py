import sys
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from answer import MODEL, client, generate
from search import search

CUTOFF = 1.05  # provisional: closest-chunk distance above this means "not in the docs"
REFUSALS = ("could not find", "couldn't find", "cannot find", "can't find")
ROUTER_PROMPT = (
    "You route questions for an assistant that answers questions about the "
    "Godot Engine documentation. Reply with exactly one word:\n"
    "DIRECT - a greeting, thanks, or a question about what the assistant can do\n"
    "CLARIFY - a request too vague to search for (for example 'it doesn't work' or 'help')\n"
    "SEARCH - anything else, including every question about Godot or game development\n\n"
    "Question: "
)


class State(TypedDict):
    question: str
    route: str
    hits: list
    best_distance: float
    answer: str


def router(state: State):
    response = client.models.generate_content(
        model=MODEL, contents=ROUTER_PROMPT + state["question"]
    )
    words = (response.text or "").strip().upper().split()
    word = words[0].strip(".:,") if words else ""
    route = word.lower() if word in ("DIRECT", "CLARIFY", "SEARCH") else "search"
    return {"route": route}


def reply_directly(state: State):
    return {
        "answer": "Hi! I answer questions about the Godot Engine manual and cite the pages I used. What would you like to know?",
        "hits": [],
    }


def ask_clarification(state: State):
    return {
        "answer": "Could you give me more detail? For example, which Godot feature or node you are working with and what you want to achieve.",
        "hits": [],
    }


def retrieve(state: State):
    hits = search(state["question"], 5)
    return {"hits": hits, "best_distance": hits[0]["distance"]}


def refuse(state: State):
    return {"answer": "I could not find that in the docs.", "hits": []}


def generate_answer(state: State):
    text = generate(state["question"], state["hits"])
    short_refusal = len(text) < 150 and any(p in text.lower() for p in REFUSALS)
    return {"answer": text, "hits": [] if short_refusal else state["hits"]}


def pick_route(state: State):
    return state["route"]


def check_relevance(state: State):
    return "answer" if state["best_distance"] <= CUTOFF else "refuse"


graph = StateGraph(State)
graph.add_node("router", router)
graph.add_node("reply_directly", reply_directly)
graph.add_node("ask_clarification", ask_clarification)
graph.add_node("retrieve", retrieve)
graph.add_node("refuse", refuse)
graph.add_node("generate_answer", generate_answer)
graph.add_edge(START, "router")
graph.add_conditional_edges(
    "router",
    pick_route,
    {"direct": "reply_directly", "clarify": "ask_clarification", "search": "retrieve"},
)
graph.add_conditional_edges(
    "retrieve", check_relevance, {"answer": "generate_answer", "refuse": "refuse"}
)
for node in ("reply_directly", "ask_clarification", "refuse", "generate_answer"):
    graph.add_edge(node, END)
app = graph.compile()


def run(question):
    return app.invoke({"question": question})


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "How do I connect a signal in GDScript?"
    result = run(question)
    print("route:", result["route"])
    if "best_distance" in result:
        print(f"closest chunk distance: {result['best_distance']:.3f} (cutoff {CUTOFF})")
    print()
    print(result["answer"])
    if result.get("hits"):
        print("\nSources:")
        for i, h in enumerate(result["hits"], 1):
            print(f"[{i}] {h['source']} (chunk {h['chunk_id']})")