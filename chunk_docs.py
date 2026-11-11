from load_docs import load_docs

MAX_CHARS = 1000

def split_long(paragraph, max_chars):
    pieces, current = [], ""
    for line in paragraph.split("\n"):
        if current and len(current) + len(line) + 1 > max_chars:
            pieces.append(current)
            current = line
        else:
            current = f"{current}\n{line}" if current else line
    if current:
        pieces.append(current)
    return pieces


def chunk_text(text, max_chars=MAX_CHARS):
    paragraphs = []
    for p in text.split("\n\n"):
        p = p.strip()
        if not p:
            continue
        if len(p) > max_chars:
            paragraphs.extend(split_long(p, max_chars))
        else:
            paragraphs.append(p)
    chunks, current = [], ""
    for p in paragraphs:
        if current and len(current) + len(p) + 2 > max_chars:
            chunks.append(current)
            current = p
        else:
            current = f"{current}\n\n{p}" if current else p
    if current:
        chunks.append(current)
    return chunks


def chunk_docs(docs):
    out = []
    for doc in docs:
        for i, chunk in enumerate(chunk_text(doc["text"])):
            out.append({"source": doc["source"], "chunk_id": i, "text": chunk})
    return out


if __name__ == "__main__":
    chunks = chunk_docs(load_docs())
    print(f"{len(chunks)} chunks")
    lengths = [len(c["text"]) for c in chunks]
    print(f"average {sum(lengths) // len(lengths)} chars, longest {max(lengths)}")
    print(chunks[5]["source"], chunks[5]["chunk_id"])
    print(chunks[5]["text"])