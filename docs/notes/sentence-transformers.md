# sentence-transformers — sentence embedding in a few lines

> A Hugging Face library that turns a whole sentence into a high-quality vector in just a few lines. Classification and similarity tasks become fast and simple.

## Why it matters

Training an embedding model yourself takes serious effort. `sentence-transformers` packages pretrained models (e.g. `all-MiniLM`, `paraphrase-mpnet`) so `encode()` returns vectors ready to use. For many problems, good embeddings plus a light classifier are enough — no need to train a large network.

## Key ideas

- **Sentence → one vector:** `encode()` returns embeddings optimized for *sentence-level* meaning comparison (not per-token vectors).
- **Fast classification:** encode sentences, then attach a light classifier (logistic / k-NN) on top — no full Transformer fine-tune required.
- **Similarity and search:** `cos_sim` finds semantically close sentences; core of [semantic-search.md](./semantic-search.md) and retrieval in [rag.md](./rag.md).
- **Load into a vector DB:** vectors from `encode()` go straight into [vector-database.md](./vector-database.md) for top-k search.
- **Pick a model for the job:** MiniLM is light and fast; mpnet is more accurate but heavier.

Quick use:

```python
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer("all-MiniLM-L6-v2")

emb = model.encode(["Hello", "Hi there"])
sim = util.cos_sim(emb[0], emb[1])   # semantic similarity
```

## Illustrations

![Cosine similarity between two sentence vectors](assets/protonx/cosine-similarity.jpg)

![Embedding: a function that maps text to vectors](assets/protonx/embeddings-function.jpg)

## Pipeline

```
sentence → SentenceTransformer.encode → vector → { cos_sim: similarity | light classifier: label | vector DB: search }
```

The shortest path from [embedding.md](./embedding.md) to [classification.md](./classification.md) and [semantic-search.md](./semantic-search.md) without heavy training.

## References

- [SBERT / sentence-transformers](https://www.sbert.net/)
- Reimers & Gurevych 2019 — [Sentence-BERT](https://arxiv.org/abs/1908.10084)

## Related

- [embedding.md](./embedding.md), [classification.md](./classification.md)
- [semantic-search.md](./semantic-search.md), [vector-database.md](./vector-database.md), [huggingface.md](./huggingface.md)
