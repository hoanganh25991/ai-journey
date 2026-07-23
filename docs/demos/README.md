# Demos = slides + working app

```
demos/<id>/
  app/index.html
  README.md
```

Catalog: [`catalog.json`](./catalog.json) — hub build reads this file.

## Concepts

| Demo | Notes |
|------|-------|
| [tokenize](./tokenize/) | `notes/tokenize.md` |
| [embedding](./embedding/) | `notes/embedding.md` |
| [attention](./attention/) | `notes/attention.md` |
| [softmax](./softmax/) | `notes/softmax.md` |
| [curve-fitting](./curve-fitting/) | `notes/curve-fitting.md` |
| [neural-networks](./neural-networks/) | `notes/neural-networks.md` |
| [rag](./rag/) | `notes/rag.md` |
| [advanced-rag](./advanced-rag/) | `notes/advanced-rag.md` |
| [mcp](./mcp/) | `notes/mcp.md` |
| [agentic-patterns](./agentic-patterns/) | `notes/agentic-patterns.md` |
| [langgraph](./langgraph/) | `notes/langgraph.md` |
| [langsmith](./langsmith/) | `notes/langsmith.md` |

## Projects

| Demo | Notes |
|------|-------|
| [self-driving-car](./self-driving-car/) | `notes/self-driving-car.md` |
| [image-gen](./image-gen/) | `notes/image-gen.md` |
| [sentiment](./sentiment/) | `notes/05-demo-text.md` |
| [complexity-router](./complexity-router/) | `notes/05-demo-text.md` |

Slides use curated images from protonx: `notes/assets/protonx/`, plus topic assets under `notes/assets/<id>/`.

```bash
./scripts/build.sh
./scripts/review.sh
```
