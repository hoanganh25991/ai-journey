# Vector database

> Store millions of embedding vectors and answer "which vectors are closest to this one?" in milliseconds. The infrastructure under RAG and semantic search.

## Why it matters

[Embedding](./embedding.md) turns everything into vectors — but where do you store them, and how do you search? Scanning every vector one by one (brute force) is too slow at scale. A vector database stores vectors with their source data and finds top-k nearest neighbors fast via approximate indexes. Without it, [RAG](./rag.md) and [semantic search](./semantic-search.md) cannot run at real-world scale.

## Key ideas

- **Core problem — nearest neighbor:** given a query vector, find the k closest by cosine or dot product ([embedding.md](./embedding.md)).
- **ANN instead of brute force:** approximate indexes (HNSW, IVF…) trade a little accuracy for orders-of-magnitude speed — good enough for search.
- **More than vectors:** each record carries *metadata* (source, date, tags) for **filtering** before or after search; needs CRUD when data changes.
- **Common choices:**
  - *FAISS* — in-memory, very fast, good for experiments; lacks durable storage and CRUD.
  - *Elasticsearch (kNN plugin)* — integrates with keyword search, has CRUD, scales out.
  - *pgvector / Chroma* — Postgres extension or lightweight store for small apps.
- **Pick by need:** scale + CRUD + distribution → Elastic; pure in-RAM speed → FAISS.

## Illustrations

![Embed the question, then query the vector store](assets/protonx/embed-then-query.jpg)

![When to use cosine vs dot product for comparing vectors](assets/protonx/cosine-vs-dot.jpg)

## Pipeline

```
documents → chunk → embedding → [vector database]
question  → embedding → [vector database: top-k search] → RAG / semantic search
```

Vector databases receive vectors from [embedding.md](./embedding.md) and supply top-k results to [rag.md](./rag.md) and [semantic-search.md](./semantic-search.md).

## References

- [FAISS (Meta)](https://github.com/facebookresearch/faiss)
- [pgvector](https://github.com/pgvector/pgvector) · [Elasticsearch kNN search](https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search.html)

## Related

- [embedding.md](./embedding.md), [rag.md](./rag.md), [semantic-search.md](./semantic-search.md)
