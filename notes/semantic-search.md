# Semantic search — hybrid · tiered · fallback

> Search by *meaning*, not just keywords, by combining two index types: inverted index (Elastic, by keyword) and semantic index (embedding, by meaning). This is the project I built to learn RAG deeply.

> Repo: [github.com/hoanganh25991/semantic-search](https://github.com/hoanganh25991/semantic-search) — Hybrid / Tiered / Fallback on the MS MARCO dataset.

## Why it matters

Keyword search (BM25 / TF-IDF in Elastic) is fast and cheap, but “car” and “automobile” are different strings — easy to miss matches. Embedding search captures meaning but is heavier to run on every query. Pragmatic semantic search **combines** both: use keywords to filter quickly, embeddings to rank by meaning. That is also a high-quality retrieve step for [RAG](./rag.md).

## Key ideas

- **Two index types:**

  | Index | Mechanism | Strong | Weak |
  |-------|-----------|--------|------|
  | **Inverted index** (Elastic) | keyword → documents | fast, cheap, precise on exact terms / IDs | no synonym understanding |
  | **Semantic index** (embedding) | vectors in [vector database](./vector-database.md) | captures meaning, varied phrasing | heavier embed + ANN cost |

- **Three search strategies:**
  - *Hybrid:* inverted index *filters* (or retrieves) candidates by keyword, semantic index *reranks* by cosine/dot. Cost-efficient when keywords hit; fails when BM25 returns empty or irrelevant candidates — semantic never sees the right docs.
  - *Tiered:* classify questions as easy/hard first → easy goes keyword-only, hard goes semantic (or hybrid). Balances p50 latency and precision (same idea as [complexity router](./05-demo-text.md)). Classifier errors are the main failure mode.
  - *Fallback:* try semantic (or hybrid) first for max accuracy; if results look poor (low scores, empty, or low confidence), *fall back* to keyword. Most accurate when tuned; most expensive on the happy path if semantic always runs first.
- **Latency shape (typical intuition):**
  - Keyword-only: ~5–30 ms (Elastic cache-warm).
  - Hybrid: keyword + embed query + rerank top-N → often ~20–80 ms.
  - Semantic-first / Fallback happy path: embed + ANN (+ optional BM25 merge) → often ~30–120 ms, plus model load cold starts.
  - Tiered: p50 near keyword; p95 near semantic — *if* the easy/hard split is calibrated.
- **Dataset and evaluation:** MS MARCO — real user questions plus relevant passages. Metrics: *Precision@k*, *MRR@10*, *Recall@k*. A query classifier labels simple vs complex questions for Tiered. Always keep a private holdout — leaderboard overfitting is real.
- **Storage:** MongoDB for raw documents; Elasticsearch for indexed data (inverted + kNN) for fast search.
- **Score fusion:** when both lists return hits, **RRF** (reciprocal rank fusion) or weighted sum of normalized BM25 + cosine beats naive “semantic only” on exact entities (order IDs, error codes).
- **Why this teaches RAG:** retrieval quality dominates answer quality — the same lesson as [rag.md](./rag.md), measured with ranking metrics instead of vibes.

## Worked example (intuition)

Question: `"How do I jump-start a car?"`

- **Keyword alone:** may miss docs that only say `"boost a vehicle battery"` (no shared tokens with “jump-start”). MRR suffers on paraphrase-heavy queries.
- **Semantic alone:** retrieves automotive battery posts, but may also surface “jump” as in *jump training* or metaphorical “jump-start your career” if the corpus is messy — high recall, noisier precision.
- **Hybrid:** BM25 keeps candidates with `battery` / `car` / `vehicle`; cosine ranks the true jump-start guide above generic car maintenance. End-to-end: keyword candidate set size ~50–200, embed once, rerank → top-10 for the UI or RAG.
- **Tiered path:** classifier marks this as *hard* (how-to, paraphrase risk) → semantic or hybrid path. A different query `"error code E42"` might be *easy* → keyword-only, sub-20 ms.
- **Fallback path:** semantic returns top score 0.22 (below threshold) → fall back to BM25 so the user still sees exact-token matches instead of an empty page.

## Common pitfalls

- **Hybrid with empty keyword hits** — need a fallback path when BM25 returns nothing (rare tokens, typos, pure paraphrase).
- **Tiered with a bad easy/hard classifier** — hard queries wrongly sent to keyword → systematic paraphrase failures; easy queries sent to semantic → wasted latency/cost.
- **Optimizing only public leaderboards** — overfit MS MARCO quirks; validate on your own corpus and languages.
- **Ignoring latency budgets** — semantic-on-everything can blow SLAs; watch p95/p99, not only mean.
- **Uncalibrated “poor result” thresholds** in Fallback — thrashing between paths or never falling back.
- **Double-counting in fusion** — merging lists without deduping doc IDs inflates scores for duplicates.

## Illustrations

![Embed the question, then query — the retrieve step of semantic search](assets/protonx/embed-then-query.jpg)

![Advanced retrieval: combine filtering and reranking for higher accuracy](assets/protonx/rag-advanced.jpg)

![Hybrid: inverted index + semantic index](assets/semantic-search/semantic-hybrid.svg)

![Two-way search flow](assets/semantic-search/search-twoway.svg)

![Hybrid vs Tiered vs Fallback strategies](assets/semantic-search/semantic-strategies.png)

## Deeper dive

- **Hybrid failure case:** query `"automobile won't crank in winter"` with a corpus that only says `"car engine fails to start in cold"`. If the keyword filter requires `"automobile"`, the candidate set is empty and reranking cannot recover — fix with synonym expansion, a looser first stage, or Fallback-to-semantic-without-filter.
- **Tiered economics:** if 70% of traffic is “easy” and keyword is 5× cheaper than semantic, Tiered can cut embed/ANN cost ~70% while holding MRR if the classifier’s false-negative rate on hard queries stays low (measure that rate explicitly).
- **Fallback latency:** worst case ≈ semantic_time + keyword_time (serial). Parallelize only if you always need both; otherwise you pay semantic on every request *and* sometimes BM25 — set a score threshold so Fallback is rare.
- **MS MARCO metric gotcha:** MRR@10 rewards getting a relevant hit near rank 1; a system can look strong on MRR while Recall@50 is mediocre — bad for RAG that needs several supporting chunks.
- **Elastic kNN + BM25:** `bool` query with `should` clauses or RRF plugin; ensure the same `_id` space so fusion isn’t comparing apples to oranges across indexes.
- **Cold-start / failure modes:** embedding model not loaded (multi-second first query), ANN index relocating shards, Mongo fetch slower than search — users blame “search quality” when the real bug is timeout → empty UI.
- **Eval loop:** fix a 200–500 query gold set from *your* logs; track Precision@5, MRR@10, p95 latency, and % path taken (keyword / hybrid / semantic / fallback) per release.

## Decision guide

| Situation | Prefer | Avoid / why |
|-----------|--------|-------------|
| Tight latency SLA, many exact-ID queries | Tiered (easy → BM25) or keyword-first Hybrid | Semantic-first Fallback on 100% traffic |
| Paraphrase-heavy how-to / natural language | Hybrid or semantic-first Fallback | Keyword-only — synonym blind spots |
| BM25 often returns 0 hits (typos, other language) | Semantic-first or Hybrid with loose/no keyword gate | Strict keyword filter before ANN |
| Need best offline quality, cost secondary | Fallback or Hybrid + cross-encoder rerank | Tiered with an untested classifier |
| Cost-sensitive high QPS | Tiered with measured easy/hard mix | Embedding every query at peak QPS |
| RAG needs diverse supporting passages | Optimize Recall@k + deduped fusion | MRR-only tuning that returns one near-duplicate |

## Pipeline

```
question → (classify easy/hard) → { keyword: inverted index | meaning: semantic index }
         → merge / rerank → top-k → RAG
```

Semantic search stands on [embedding.md](./embedding.md) + [vector-database.md](./vector-database.md), and is the retrieval step for [rag.md](./rag.md).

## Slides & demo

| | Link |
|--|------|
| Slides | [slides/semantic-search](../slides/semantic-search/index.html) |
| GitHub | [hoanganh25991/semantic-search](https://github.com/hoanganh25991/semantic-search) |

## References

- Repo: [hoanganh25991/semantic-search](https://github.com/hoanganh25991/semantic-search)
- [MS MARCO](https://microsoft.github.io/msmarco/) · [Elasticsearch kNN](https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search.html)

## Related

- [vector-database.md](./vector-database.md), [rag.md](./rag.md), [embedding.md](./embedding.md)
- [05-demo-text.md](./05-demo-text.md) — complexity router (same tiered idea)
