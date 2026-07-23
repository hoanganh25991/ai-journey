# AI Journey — Notes Index

> **Source of truth = English notes.** Each topic is a `.md` file with a short explanation. Build the static hub in `docs/` and open or serve from there. Vietnamese is **not** stored in separate files — the built site translates EN → VI at runtime in the browser.

Build: `./scripts/build.sh` → open [`../docs/index.html`](../docs/index.html). Review like GitHub Pages: `./scripts/review.sh`.

Catalog: [`catalog.json`](./catalog.json) — listing source of truth (id, title, summary, slides, demo).

**Start here:** open the hub → **Journey** (`docs/journey.html`) — a fun five-stage map. Journey is a **separate presentation**, not a note.

## Three layers of content (+ journey)

| Class | Role | When to read |
|-------|------|--------------|
| **Note** (`.md`) | Simplest place to get the main idea | always start here |
| **Journey** (`journey.html`) | Fun map connecting notes by level | want the big picture / pick a route |
| **Slide** (`slides/<topic>/`) | Present with pictures + step by step | re-lecture / present |
| **Demo** (`demos/<topic>/app/`) | Try it in the browser | want to *feel* how it runs |

A note is the center; it may link to a slide and a demo (declared in `catalog.json`; use `null` if missing).

## Language

- **Author and edit in English** under `notes/`.
- **VI in the browser:** after `./scripts/build.sh`, use the EN/VI toggle on built pages — translation calls a public web API client-side (same approach as `build-docs.py`, no parallel `-vi.md` files).

## Note writing conventions

Each note follows the same framework:

1. Title + lead sentence (everyday example).
2. **Why it matters** — short paragraph.
3. **Key ideas** — 3–5 bullets with small examples.
4. **Illustrations** — 1–3 images, each with a caption (when applicable).
5. **Pipeline** — connect to the next note.
6. **Slides & demo** — link table (when applicable).
7. **References** — 1–3 public links (optional).
8. **Related** — links to sibling notes.

## Insert image/PDF into a note

Photos are the fastest way to make an idea clear:

```
screenshot / PDF page  →  notes/assets/<topic>/filename.jpg
                       →  in note: ![short caption](assets/<topic>/filename.jpg)
                       →  ./scripts/build.sh  →  docs/notes/*.html
```

- Copy the image to `notes/assets/…` and reference it with the **relative** path `assets/…` — build copies assets to `docs/notes/assets/` for local and GitHub Pages.
- Image on its own line → becomes `<figure>` with caption from `![…]`.
- **Complex PDF:** do not embed the whole file. Capture 1–2 key pages as images, or link externally; write the core idea in prose in the note.

## Notes

| Notes | Group | Slides | Demo |
|-------|-------|--------|------|
| [tokenize.md](./tokenize.md) | concepts | yes | yes |
| [embedding.md](./embedding.md) | concepts | yes | yes |
| [attention.md](./attention.md) | concepts | yes | yes |
| [softmax.md](./softmax.md) | concepts | yes | yes |
| [classification.md](./classification.md) | concepts | yes | — |
| [curve-fitting.md](./curve-fitting.md) | concepts | yes | yes |
| [neural-networks.md](./neural-networks.md) | concepts | yes | yes |
| [pytorch-training.md](./pytorch-training.md) | concepts | yes | — |
| [tensorflow-training.md](./tensorflow-training.md) | concepts | yes | — |
| [huggingface.md](./huggingface.md) | concepts | yes | — |
| [kaggle.md](./kaggle.md) | concepts | yes | — |
| [transformer.md](./transformer.md) | concepts | yes | — |
| [sentence-transformers.md](./sentence-transformers.md) | concepts | yes | — |
| [rag.md](./rag.md) | concepts | yes | yes |
| [advanced-rag.md](./advanced-rag.md) | concepts | yes | yes |
| [vector-database.md](./vector-database.md) | concepts | yes | — |
| [semantic-search.md](./semantic-search.md) | projects | yes | GitHub |
| [mcp.md](./mcp.md) | concepts | yes | yes |
| [skills-rules.md](./skills-rules.md) | concepts | yes | mcp app |
| [train-gpu.md](./train-gpu.md) | concepts | yes | — |
| [self-driving-car.md](./self-driving-car.md) | projects | yes | yes |
| [image-gen.md](./image-gen.md) | projects | yes | yes |
| [05-demo-text.md](./05-demo-text.md) | projects | yes | yes (+ complexity-router) |
| [06-train-infer.md](./06-train-infer.md) | concepts | yes | — |
| [07-agents.md](./07-agents.md) | concepts | yes | mcp app |
| [agentic-patterns.md](./agentic-patterns.md) | concepts | yes | yes |
| [langgraph.md](./langgraph.md) | concepts | yes | yes |
| [langsmith.md](./langsmith.md) | concepts | yes | yes |
| [08-model-notes.md](./08-model-notes.md) | field-notes | yes | — |
| [09-agent-automation.md](./09-agent-automation.md) | field-notes | Hermess | — |
| [10-ai-timeline.md](./10-ai-timeline.md) | field-notes | yes | — |
| [personal-knowledge-base.md](./personal-knowledge-base.md) | projects | overview | CLI / plan |

## Assets

[`assets/`](./assets/) — illustrations for notes and slides. Add new images by topic, then rebuild.
