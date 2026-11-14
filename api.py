from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from agent import run

app = FastAPI(title="Godot Docs Assistant")


class Question(BaseModel):
    question: str = Field(min_length=1, max_length=500)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask(body: Question):
    try:
        result = run(body.question)
    except Exception:
        raise HTTPException(status_code=503, detail="The language model is unavailable. Try again shortly.")
    return {
        "route": result["route"],
        "answer": result["answer"],
        "sources": [
            {"source": h["source"], "chunk_id": h["chunk_id"]}
            for h in result.get("hits", [])
        ],
    }