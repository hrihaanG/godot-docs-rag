from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")
print("max tokens per input:", model.max_seq_length)

sentences = [
    "How do I move a character with the keyboard?",
    "Use the Input class to read key presses and move the player.",
    "Shaders are programs that run on the GPU.",
]
vectors = model.encode(sentences)
print("vector shape:", vectors.shape)
print("question vs relevant:", util.cos_sim(vectors[0], vectors[1]).item())
print("question vs unrelated:", util.cos_sim(vectors[0], vectors[2]).item())