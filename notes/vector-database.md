# Vector database

> Store millions of embedding vectors and answer “which vectors are closest to this one?” in milliseconds. The infrastructure under RAG and semantic search. Everyday metaphor: a library that shelves books by *meaning coordinates*, not only by title keywords — and can point to the nearest shelves instantly.

## Why it matters

[Embedding](./embedding.md) turns everything into vectors — but where do you store them, and how do you search? Scanning every vector one by one (brute force) is too slow at scale. A vector database stores vectors with their source data and finds top-k nearest neighbors fast via approximate indexes. Without it, [RAG](./rag.md) and [semantic search](./semantic-search.md) cannot run at real-world scale.

## Key ideas

- **Core problem — nearest neighbor:** given a query vector, find the k closest by cosine or dot product ([embedding.md](./embedding.md)).
- **ANN instead of brute force:** approximate indexes (HNSW, IVF…) trade a little accuracy for orders-of-magnitude speed — good enough for search.
- **More than vectors:** each record carries *metadata* (source, date, tags) for **filtering** before or after search; needs CRUD when documents change.
- **Chunking first:** you rarely embed a whole book as one vector — split into passages, embed each, store chunk text + vector + metadata together.
- **Common choices:**
  - *FAISS* — in-memory, very fast, good for experiments; lacks durable storage and rich CRUD out of the box.
  - *Elasticsearch (kNN plugin)* — integrates with keyword search, has CRUD, scales out — natural fit for hybrid search.
  - *pgvector / Chroma* — Postgres extension or lightweight store for small apps and local demos.
- **Pick by need:** scale + CRUD + distribution → Elastic; pure in-RAM speed / research → FAISS; simple app → pgvector/Chroma.
- **Metric must match training:** if embeddings were trained with cosine, search with cosine (or normalize + dot). Wrong metric → wrong ranking.

## Worked example (intuition)

1. Split docs into ~200–400 token chunks.
2. `encode()` each chunk with [sentence-transformers](./sentence-transformers.md).
3. Upsert `(vector, text, source, date)` into the DB.
4. On question: embed question → ANN top-8 → optional metadata filter (`date > 2024`) → hand chunks to the LLM ([rag.md](./rag.md)).

## Common pitfalls

- **Stale index** — docs changed but vectors not re-embedded.
- **Dimension / model mismatch** — query encoder ≠ index encoder.
- **No metadata filters** — retrieving irrelevant years/sources.
- **k too small or too large** — miss context, or drown the LLM in noise.

## Illustrations

![Embed the question, then query the vector store](assets/protonx/embed-then-query.jpg)

![When to use cosine vs dot product for comparing vectors](assets/protonx/cosine-vs-dot.jpg)

![ANN nearest-neighbor search visualization](assets/vector-database/vector-db-ann.png)

![Index once, query many times](assets/vector-database/vector-db-flow.svg)


![Retrieve detail: chunks → ANN → top-k](assets/vector-database/vector-retrieve-detail.png)

## Pipeline

```
documents → chunk → embedding → [vector database]
question  → embedding → [vector database: top-k search] → RAG / semantic search
```

Vector databases receive vectors from [embedding.md](./embedding.md) / [sentence-transformers.md](./sentence-transformers.md) and supply top-k results to [rag.md](./rag.md) and [semantic-search.md](./semantic-search.md).

## Slides & demo

| | Link |
|--|------|
| Slides | [slides/vector-database](../slides/vector-database/index.html) |
| Related demo | [demos/rag](../demos/rag/app/index.html) |

## References

- [FAISS (Meta)](https://github.com/facebookresearch/faiss)
- [pgvector](https://github.com/pgvector/pgvector) · [Elasticsearch kNN search](https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search.html)

## Related

- [embedding.md](./embedding.md), [rag.md](./rag.md), [semantic-search.md](./semantic-search.md)
- [sentence-transformers.md](./sentence-transformers.md)
