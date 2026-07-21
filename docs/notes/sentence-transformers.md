# sentence-transformers — sentence embedding in a few lines

> A Hugging Face library that turns a whole sentence into a high-quality vector in just a few lines. Classification and similarity tasks become fast and simple. Everyday metaphor: instead of weighing every letter, you stamp the whole postcard into one coordinate on a meaning map.

## Why it matters

Training an embedding model yourself takes serious effort. `sentence-transformers` packages pretrained models (e.g. `all-MiniLM`, `paraphrase-mpnet`) so `encode()` returns vectors ready to use. For many problems, good embeddings plus a light classifier are enough — no need to fine-tune a large network.

This is the shortest path from [embedding.md](./embedding.md) into [semantic-search.md](./semantic-search.md), [vector-database.md](./vector-database.md), and retrieval for [rag.md](./rag.md).

## Key ideas

- **Sentence → one vector:** `model.encode(texts)` returns a matrix `n × d` optimized for *sentence-level* meaning comparison (not raw per-token hidden states). Internally: Transformer → **pooling** → optional L2 normalize.
- **Pooling choices matter:**
  - *Mean pooling* (default for many MiniLM/mpnet checkpoints): average token states, often masked so padding does not dilute the vector.
  - *CLS pooling:* take the `[CLS]` token (BERT-style) — only good if the checkpoint was trained that way.
  - *Max pooling:* element-wise max — less common for modern SBERT models.
  - Wrong pooling on a checkpoint = systematic similarity bugs even when dimensions “look right.”
- **Fast classification:** encode sentences once, then attach logistic regression / k-NN / a tiny MLP on frozen vectors — often enough for topic or intent labels without full Transformer fine-tune.
- **Similarity and search:** `util.cos_sim(a, b)` (or dot on normalized vectors) ranks paraphrases; core of semantic search and RAG retrieve. Typical demo dims: **384** (`all-MiniLM-L6-v2`) or **768** (`all-mpnet-base-v2`).
- **Load into a vector DB:** `encode()` output goes straight into FAISS / pgvector / Elastic kNN — store the *same* `d` and metric the model expects ([vector-database.md](./vector-database.md)).
- **Pick a model for the job:**
  - *`all-MiniLM-L6-v2`* — ~22M params, 384-d, very fast CPU; strong default for demos and medium corpora.
  - *`all-mpnet-base-v2`* — ~110M params, 768-d; usually higher retrieval quality, slower/heavier.
  - *`multi-qa-*` / asymmetric models* — trained for question→passage; better when queries are short and docs are long.
  - *Multilingual* (`paraphrase-multilingual-MiniLM-L12-v2`, `distiluse-base-multilingual-cased-v2`, etc.) when queries and docs mix languages — English-only MiniLM will quietly fail on Vietnamese/French text.
  - *E5 / BGE / GTE* families (also loadable via SBERT or `transformers`) — strong MTEB retrieval scores; check whether they want `"query: "` / `"passage: "` prefixes.
- **Same space for query and docs:** encode both with the **same checkpoint and same prompts/prefixes**. Never mix two incompatible models in one index — dimensions and geometry will not match.

## Quick use

```python
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")
emb = model.encode(
    ["Hello", "Hi there", "Battery life is awful"],
    normalize_embeddings=True,  # safe for cosine == dot
)
print(util.cos_sim(emb[0], emb[1]))  # high — greetings (~0.7–0.9)
print(util.cos_sim(emb[0], emb[2]))  # lower — different topic (~0.0–0.3)
```

## Worked example (intuition)

Corpus: 5,000 FAQ answers, ~80–200 tokens each.

1. **Offline index build:** `model.encode(faqs, batch_size=64, show_progress_bar=True)` → `5000 × 384` float32 matrix (~7.3 MB raw). On a laptop CPU, MiniLM often does thousands of short sentences per minute; on GPU, large corpora finish in seconds to minutes.
2. **Store:** push vectors + FAQ text + `faq_id` into FAISS (`IndexFlatIP` after L2-normalize) or Chroma/pgvector.
3. **Query:** user asks `"How do I reset my password?"` → encode **one** vector (milliseconds) → top-5 by cosine.
4. **RAG handoff:** concatenate the 5 FAQ bodies into the LLM context ([rag.md](./rag.md)). The heavy Transformer ran once per document at index time; each live query is one short encode + ANN lookup.
5. **Multilingual twist:** if half the FAQs are Vietnamese, switch to a multilingual checkpoint and **rebuild the whole index** — you cannot bolt vi queries onto an English-only MiniLM space.

## Common pitfalls

- **Mixing models in one index** — dimensions and geometry won’t match; top-k becomes noise.
- **Using token embeddings as if they were sentence vectors** — wrong pooling; similarity collapses.
- **Cosine vs dot without normalizing** — rankings shift; know which metric your DB expects.
- **Encoding huge batches on CPU only** — fine for tiny demos; use GPU + batched `encode` for large corpora.
- **Ignoring instruction prefixes** (E5/BGE-style) — retrieval drops several points if you forget `query:` vs `passage:`.
- **Assuming multilingual “just works”** with English-only weights — cross-lingual nearest neighbors are unreliable.

## Illustrations

![Cosine similarity between two sentence vectors](assets/protonx/cosine-similarity.jpg)

![Embedding: a function that maps text to vectors](assets/protonx/embeddings-function.jpg)

![Sentence embedding and cosine angle](assets/sentence-transformers/sentence-embed.png)

## Deeper dive

- **SBERT training idea:** siamese/triplet fine-tune of a pretrained encoder so cosine distance matches labeled similarity (NLI, paraphrase, MS MARCO). Vanilla BERT CLS vectors are weak at sentence similarity without this step — that is why `sentence-transformers` exists.
- **API surface:** `SentenceTransformer.encode(sentences, batch_size=32, convert_to_numpy=True, normalize_embeddings=False)`. Set `normalize_embeddings=True` when the vector DB uses inner product and you want cosine ranking.
- **Throughput ballpark:** `all-MiniLM-L6-v2` on a modern CPU might embed ~500–2000 short sentences/sec depending on length; GPU (e.g. T4) often 5–20× that. Profile on *your* chunk length — 512-token chunks are far slower than 64-token titles.
- **Matryoshka / truncation:** some newer models allow using only the first 256 dims with small quality loss — useful when FAISS RAM dominates. Do not truncate arbitrary MiniLM vectors unless the card says it is trained for that.
- **Failure mode — domain shift:** general MiniLM on legal/medical jargon clusters poorly. Fix: domain fine-tune with MultipleNegativesRankingLoss on your query–passage pairs, or pick a domain checkpoint.
- **Asymmetric retrieval:** short query vs long passage — models trained with `MultipleNegativesRankingLoss` on QA pairs beat symmetric paraphrase models on FAQ search; the reverse is true for “find duplicate sentences.”
- **Multilingual pitfall:** `paraphrase-multilingual-*` shares one space across languages, but quality is uneven by language; always measure Recall@k on *your* language pair, not only English MTEB headlines.

## Decision guide

| Situation | Prefer | Avoid / why |
|-----------|--------|-------------|
| Demo / laptop / <100k chunks | `all-MiniLM-L6-v2` (384-d) | mpnet or 7B embedders — latency and RAM without need |
| Max retrieval quality, English FAQ/RAG | `all-mpnet-base-v2` or strong E5/BGE | Random Hub model with no retrieval training |
| Mixed-language corpus or queries | Multilingual SBERT / multilingual-E5 | English-only MiniLM — silent quality cliff |
| Question → long passage search | `multi-qa-*` or asymmetric E5 (`query:`/`passage:`) | Symmetric paraphrase model alone |
| Real-time embed on every keystroke | MiniLM + batch/cache; or smaller distilled embedder | Re-encoding the full corpus per keystroke |
| Metric in DB is inner product | L2-normalize in `encode` (cosine ≡ dot) | Raw unnormalized vectors with IP — magnitude dominates |

## Pipeline

```
sentence → SentenceTransformer.encode → vector → { cos_sim | light classifier | vector DB }
```

## Slides & demo

| | Link |
|--|------|
| Slides | [slides/sentence-transformers](../slides/sentence-transformers/index.html) |
| Related demo | [demos/embedding](../demos/embedding/app/index.html) |

## References

- [SBERT / sentence-transformers](https://www.sbert.net/)
- Reimers & Gurevych 2019 — [Sentence-BERT](https://arxiv.org/abs/1908.10084)

## Related

- [embedding.md](./embedding.md), [classification.md](./classification.md)
- [semantic-search.md](./semantic-search.md), [vector-database.md](./vector-database.md), [huggingface.md](./huggingface.md)
