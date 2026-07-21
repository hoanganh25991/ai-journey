# Personal Knowledge-Base — Videos · Docs · GitHub

> **Separate repo:** [`~/work-station/personal-kb`](../../personal-kb)  
> Will attach to ai-journey as a **git submodule** (not added yet — run tooling from the sibling path).

The hub `index.html` searches **notes** only. Personal Knowledge-base searches videos / GitHub / work-station files plus **Graph RAG** (linked keywords).

## Why it matters

Notes explain concepts; personal-kb is where my own corpus lives — saved videos, starred repos, local docs — with search and a keyword graph for discovery. It is the practical RAG playground described in [rag.md](./rag.md).

## Key ideas

- **Run locally:**

  ```bash
  cd ~/work-station/personal-kb
  python3 scripts/build-kb-index.py
  python3 scripts/build-keyword-graph.py
  python3 scripts/kb-search.py "first mate"
  python3 ui/server.py
  # → http://127.0.0.1:8765/      search
  # → http://127.0.0.1:8765/graph Graph RAG (round nodes, zoom, click)
  ```

- **Docs in the knowledge-base repo:**
  - [README](../../personal-kb/README.md)
  - [Sources](../../personal-kb/data/SOURCES.md)
  - [Plan](../../personal-kb/plans/knowledge-base.md)

- **Graph UI:** [graph.html](../../personal-kb/ui/public/graph.html)

## Pipeline

```
ingest videos / docs / GitHub → FTS index + keyword graph → search / Graph RAG
```

## Slides & demo

| | Link |
|--|------|
| Slides | [slides/personal-knowledge-base](../slides/personal-knowledge-base/index.html) |
| Knowledge-base README | [../personal-kb/README.md](../../personal-kb/README.md) |
| Plan | [../personal-kb/plans/knowledge-base.md](../../personal-kb/plans/knowledge-base.md) |
| Graph UI | [../personal-kb/ui/public/graph.html](../../personal-kb/ui/public/graph.html) |

## Related

- [rag.md](./rag.md), [embedding.md](./embedding.md), [07-agents.md](./07-agents.md)
