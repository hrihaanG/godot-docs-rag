# Godot Docs Assistant

A small retrieval-augmented question-answering app over the Godot Engine manual. It retrieves the most relevant passages and has an LLM answer from them, with citations. Work in progress.

**Unofficial:** this project is not affiliated with or endorsed by the Godot Engine project.

## Evaluation

See [EVALUATION.md](EVALUATION.md) for retrieval and answer results, failure cases and caveats.

## Attribution

This project uses the *Godot Engine documentation* by Juan Linietsky, Ariel Manzur and the Godot community, available at [godotengine/godot-docs](https://github.com/godotengine/godot-docs) and licensed under [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/). The documentation itself is not included in this repository.

**Changes made:** the original text has been modified. It is split into chunks, and excerpts are quoted in answers and in the evaluation files. Only the `getting_started` and `tutorials` folders are used.

This project is not affiliated with or endorsed by the Godot Engine project or the original authors.

Setup and run instructions will be added once the API and Docker image are done.
