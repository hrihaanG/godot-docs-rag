# Evaluation

Evaluated 14 Nov 2026. This document reports what the Godot Docs Assistant gets right, where it fails, and how much the numbers can be trusted.

## What was tested

- **Documents:** the Godot manual (`getting_started` and `tutorials` folders), 434 `.rst` files.
- **Chunking:** split at blank lines, with long paragraphs split at line breaks, to at most 500 characters. This gives 12,251 chunks (average 394 characters, about 125 tokens).
- **Retrieval:** `all-MiniLM-L6-v2` embeddings (384 numbers per chunk) stored in Chroma. The app retrieves the 5 closest chunks.
- **Answering:** `gemini-3.5-flash-lite` on the free tier. The prompt tells the model to answer only from the numbered excerpts, cite them as [n], and say so when the answer is not in them.
- **Test set:** 18 questions in `eval_questions.json`: 16 answerable and 2 out of scope. Six were chosen from pages seen during development. Ten were written from pages sampled at random (seed 42). Each answerable question lists the expected page(s) and keywords.

## Retrieval results (16 answerable questions)

| | Page level | Chunk level |
|---|---|---|
| hit@1 | 11 / 16 | 8 / 16 |
| hit@3 | 12 / 16 | 12 / 16 |
| hit@5 | 14 / 16 | 13 / 16 |
| hit@10 | 14 / 16 | 14 / 16 |

- **Page level:** a chunk from an expected page appears in the top k.
- **Chunk level:** a chunk from an expected page that also contains at least one of the question's keywords appears in the top k. This is stricter, because a right page can match while the chunk with the answer is missed.
- The headline figure is hit@5, since the app reads 5 chunks: **87.5% at page level and 81% at chunk level**.
- Top-1 alone is unreliable: for three questions the right page ranked first but the chunk with the answer ranked second.

## Answer results (single run)

- **Answerable questions:** 12 of 16 passed. A pass means the answer does not refuse, contains all the keywords, cites an expected page, and uses valid citation numbers.
- **Out-of-scope questions:** 2 of 2 were refused.
- An earlier run on `gemini-3.8-flash` also scored 12 of 16, but two questions got no answer because the free-tier daily request limit was reached. The two runs are not directly comparable.

## Failure cases

| Question | What happened | Cause |
|---|---|---|
| What does the green icon next to a function in the script editor mean? | The model said it could not find a green icon. | Retrieval. The chunk that answers it ranked 26th, so the model never saw it. A keyword search for the exact phrase would find it. |
| What is godot-cpp? | The model described the API and never gave the definition. | Retrieval. The definition chunk ranked 14th, outside the top 5. |
| What stretch mode and aspect should I set for a 2D game? | The model answered stretch mode `canvas_items` and aspect `expand`. The 2D tutorial uses `keep`. | Ambiguous question. Retrieval returned another page on the same topic, which gives different advice. |
| How do I make a character jump in 2D? | The answer gave the jump condition and the velocity line but left out `move_and_slide()`, which applies the velocity, and it mixed in 3D context. | Incomplete answer. The same question passed in the earlier run, and a single run cannot show whether the difference comes from the model or from randomness. |
| How do I add an animation in GDScript? (asked while testing the Docker container; not one of the 18 test questions) | The model said it could not find the answer. | Retrieval. The top 5 chunks were two from AnimationTree, a scripting intro, a page on scene instances and 3D movement code. Pages on sprite animation and the animation introduction ranked 6th and 7th, just outside the top 5. The question is also vague about which kind of animation. |

## Other issues found

- **Tables:** large tables have no blank lines, so the first chunker produced chunks up to 61,649 characters. These are now split at line breaks, but split tables lose their header rows.
- **Token limit:** 776 of 12,251 chunks (6%) exceed the embedding model's 256-token limit, so their tails are not embedded.
- **Markup:** `.rst` comments, labels and directives remain inside chunks.
- **2D and 3D:** the small embedding model barely separates "2D" from "3D", so 3D pages can outrank 2D ones for 2D questions.
- **Out-of-scope questions:** retrieval always returns 5 chunks, so a refusal still lists 5 sources.
- **Code tabs:** chunks can contain both GDScript and C# versions of the same code, and answers can blend the two languages.
- **Citations:** a citation can be correct while the answer still mislabels a detail.

## Routing graph (LangGraph)

`agent.py` wraps the pipeline in a small workflow. A router labels each question as direct (greeting), clarify (too vague) or search. Searches go through retrieval, then a distance check: if the closest chunk is farther than 1.05, the app refuses without calling the model. Otherwise the model answers, and if it gives a short "could not find" reply, the source list is dropped. This is a routed workflow with fixed steps, not an autonomous agent.

Run on the same 18 questions (single run, `gemini-3.5-flash-lite`): 12 / 16 answerable passed and 2 / 2 out-of-scope were refused, the same as the plain pipeline, with the same four failures. All 16 answerable questions were routed to search, and none was refused by the distance check.

Limits of the distance check: the cutoff of 1.05 was chosen from 10 questions (5 on-topic, 5 off-topic). It separates unrelated questions (France 1.163, Unity 1.099) from Godot questions, but not questions about other game engines: an Unreal Engine question scored 0.900, inside the range of hard Godot questions (0.91 to 0.97). For those, the prompt rule is the only protection, and it was checked on a single run.

## How much to trust these numbers

- There are only 16 answerable questions, so one question moves a percentage by about 6 points.
- Ten questions were written after reading the opening of each page and reuse its wording, so they are probably easier than real user questions.
- The keyword check is crude. It can pass a wrong answer that contains the word and fail a right answer phrased differently.
- Each model was run once, and language model output varies between runs.
- **A labelling mistake, reversed:** during development, two expected-page labels were widened after the results had been seen, which raised hit@5 to 16/16. That was reversed, because counting a whole page hid cases where the chunk with the answer was never retrieved. All numbers above use the original labels.

## What to try next

- Hybrid search, combining keyword matching with vector search, to catch exact phrases such as "green icon".
- A larger top-k with re-ranking.
- Stripping `.rst` markup before chunking, and repeating header rows when a table is split.
- Repeating the answer evaluation several times and reporting the spread.
