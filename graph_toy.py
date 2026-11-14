from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    question: str
    route: str
    answer: str


def router(state: State):
    q = state["question"].lower().strip()
    if q in ("hi", "hello", "hey"):
        return {"route": "direct"}
    return {"route": "search"}


def reply_directly(state: State):
    return {"answer": "Hello! Ask me anything about the Godot docs."}


def search_docs(state: State):
    return {"answer": f"(would search the docs for: {state['question']})"}


def pick(state: State):
    return state["route"]


graph = StateGraph(State)
graph.add_node("router", router)
graph.add_node("reply_directly", reply_directly)
graph.add_node("search_docs", search_docs)
graph.add_edge(START, "router")
graph.add_conditional_edges(
    "router", pick, {"direct": "reply_directly", "search": "search_docs"}
)
graph.add_edge("reply_directly", END)
graph.add_edge("search_docs", END)
app = graph.compile()

for q in ["hello", "How do I connect a signal?"]:
    print(q, "->", app.invoke({"question": q})["answer"])