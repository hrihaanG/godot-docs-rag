import os
import sys

from dotenv import load_dotenv
from google import genai

from search import search

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-3.5-flash-lite"


def generate(question, hits):
    context = "\n\n".join(
        f"[{i}] (source: {h['source']})\n{h['text']}"
        for i, h in enumerate(hits, 1)
    )
    prompt = (
        "You are an assistant for the Godot Engine documentation.\n"
        "Answer the question using ONLY the numbered excerpts below. "
        "Cite the excerpts you used like [1] or [2]. "
        "If the excerpts do not contain the answer, say you could not "
        "find it in the docs.\n\n"
        f"Excerpts:\n{context}\n\nQuestion: {question}"
    )
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text


def answer(question, k=5):
    hits = search(question, k)
    return generate(question, hits), hits


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "How do I connect a signal in GDScript?"
    text, hits = answer(question)
    print(text)
    print("\nSources:")
    for i, h in enumerate(hits, 1):
        print(f"[{i}] {h['source']} (chunk {h['chunk_id']})")