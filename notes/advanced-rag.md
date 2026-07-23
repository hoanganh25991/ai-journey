# Advanced RAG — Query Translation & Beyond

> Basic RAG embeds the user question as-is. Advanced RAG *rewrites* the question (and sometimes the index) so retrieval finds the right chunks: multi-query, fusion, HyDE, step-back, routing, RAPTOR, ColBERT. Everyday metaphor: a librarian who rephrases your vague ask before searching the stacks.

## Why it matters

[rag.md](./rag.md) gets you grounded answers. Failures usually sit in **retrieval**, not generation. The “RAG from scratch” playbook is a toolbox of query (and index) transforms — pick one when the naive top-k is wrong.

## Key ideas

- **Query translation family**
  - *Multi-query* — several paraphrases → union of hits.
  - *RAG-Fusion* — rank-fuse results from those queries.
  - *Decomposition* — split a hard question into sub-questions.
  - *Step-back* — ask a more abstract question first, then retrieve.
  - *HyDE* — invent a hypothetical answer doc, embed *that*, search.
- **Routing & structuring:** send the question to the right index / filter (metadata, SQL-like structure) instead of one flat store.
- **Index-side upgrades:** multi-representation indexing, RAPTOR (cluster summaries), ColBERT (late interaction) — better recall when chunks alone are weak.
- **Self-reflective RAG:** retrieve → critique → rewrite / re-retrieve (pairs well with [langgraph.md](./langgraph.md)).

## Pipeline

```
question → (translate / route / structure) → retrieve → (optional reflect) → generate + cite
```

## Slides & demo

| | Link |
|--|------|
| Slides | [slides/advanced-rag](../slides/advanced-rag/index.html) |
| App | [demos/advanced-rag/app](../demos/advanced-rag/app/index.html) |

## References

- LangChain — RAG From Scratch series
- Lewis et al. 2020 — RAG; ColBERT / RAPTOR papers as named techniques

## Related

- [rag.md](./rag.md), [vector-database.md](./vector-database.md), [semantic-search.md](./semantic-search.md)
- [langgraph.md](./langgraph.md) — graph the reflective loop
