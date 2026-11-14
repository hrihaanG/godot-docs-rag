from search import search

ON_TOPIC = [
    "How do I make a character run in Godot?",
    "How do I create a new scene in Godot?",
    "How do I add a sprite to my scene?",
    "How do I handle input in Godot?",
    "How do I play an animation in Godot?",
]
OFF_TOPIC = [
    "How do I make a character run in Unity?",
    "How do I create a new scene in Unreal Engine?",
    "How do I add a sprite to my scene in Blender?",
    "How do I mod a game in creation engine?",
    "What is the best way to learn programming in Python?",
]

for label, questions in (("on-topic", ON_TOPIC), ("off-topic", OFF_TOPIC)):
    for q in questions:
        best = search(q, k=1)[0]["distance"]
        print(f"{best:.3f}  {label:<9} {q[:70]}")