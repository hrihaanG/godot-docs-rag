from pathlib import Path

DOCS_DIR = Path("data/godot-docs")
FOLDERS = ["getting_started", "tutorials"]


def load_docs():
    docs = []
    for folder in FOLDERS:
        for path in (DOCS_DIR / folder).rglob("*.rst"):
            text = path.read_text(encoding="utf-8")
            docs.append({
                "source": path.relative_to(DOCS_DIR).as_posix(),
                "text": text,
               })
    return docs


if __name__ == "__main__":
    docs = load_docs()
    print(f"Loaded {len(docs)} files")
    print(f"Total characters: {sum(len(d['text']) for d in docs)}")
    print(docs[0]["source"])
    print(docs[0]["text"][:300])