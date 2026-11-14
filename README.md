# Godot Docs Assistant

A small retrieval-augmented question-answering app over the Godot Engine manual. It retrieves the most relevant passages and has an LLM answer from them, with citations. Work in progress.

**Unofficial:** this project is not affiliated with or endorsed by the Godot Engine project.

## Evaluation

See [EVALUATION.md](EVALUATION.md) for retrieval and answer results, failure cases and caveats.

## Attribution

The Godot documentation is by Juan Linietsky, Ariel Manzur and the Godot community, licensed under [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/). It is not included in this repository; get it from [godotengine/godot-docs](https://github.com/godotengine/godot-docs). This project splits the text into chunks and quotes excerpts in answers and evaluation files, so those are adapted material. Only the `getting_started` and `tutorials` folders are used.

Setup and run instructions will be added once the API and Docker image are done.
