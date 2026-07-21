# Demos = slides + working app

```
demos/<id>/
  slides/index.html
  app/index.html
  README.md
```

Catalog: [`catalog.json`](./catalog.json) — Unified UI reads this file.

## Concepts

| Demo | Notes |
|------|-------|
| [tokenize](./tokenize/) | `notes/tokenize.md` |
| [embedding](./embedding/) | `notes/embedding.md` |
| [attention](./attention/) | `notes/attention.md` |
| [softmax](./softmax/) | `notes/softmax.md` |
| [rag](./rag/) | `notes/rag.md` |
| [mcp](./mcp/) | `notes/mcp.md` |

## Projects

| Demo | Notes |
|------|-------|
| [car-nn](./car-nn/) | `notes/04-demo-car.md` |
| [sentiment](./sentiment/) | `notes/05-demo-text.md` |
| [complexity-router](./complexity-router/) | `notes/05-demo-text.md` |

Slides use curated images from protonx: `notes/assets/protonx/`.

```bash
python3 ui/server.py
# → http://127.0.0.1:8765
```
