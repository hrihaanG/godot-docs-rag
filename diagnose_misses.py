from search import search

CASES = [
    (5, "What does the green icon next to a function in the script editor mean?",
     "green icon", "getting_started/first_2d_game/03.coding_the_player.rst"),
    (6, "What stretch mode and aspect should I set so my 2D game scales on different screen sizes?",
     "canvas_items", "getting_started/first_2d_game/01.project_setup.rst"),
    (16, "What is godot-cpp?",
     "official c++ gdextension bindings", "tutorials/scripting/cpp/about_godot_cpp.rst"),
]

for qid, question, phrase, page in CASES:
    hits = search(question, k=30)
    print(f"#{qid} phrase '{phrase}':")
    for i, h in enumerate(hits, 1):
        if phrase in h["text"].lower().replace("\n", " "):
            mark = "  <-- expected page" if h["source"] == page else ""
            print(f"   rank {i}: {h['source']}{mark}")