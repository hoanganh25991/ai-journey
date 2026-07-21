# Demo: Sentiment & Complexity routing

> Two text demos share one idea: read a sentence and *label* it. Sentiment labels emotion; the complexity router labels easy vs hard to pick how to handle the request.

## Why it matters

This is where tokenize → embedding → softmax runs end-to-end on real sentences. Classification is not only "guess the mood" — it also *routes* the system: easy queries get a fast path, hard ones mobilize heavier agents.

## Key ideas

- **Sentiment (emotion classification):** three classes — negative / neutral / positive. Same chain: [tokenize.md](./tokenize.md) → [embedding.md](./embedding.md) → [softmax.md](./softmax.md).
- **Complexity router (difficulty routing):** classify requests as simple or complex, then route — simple to a fast/cheap model, complex to a multi-agent crew or first-mate.
- **Same shape, different purpose:** both are classification; the label drives different downstream behavior — display sentiment vs choose the next path.
- **Routing saves cost:** not every sentence needs the strongest model; the router balances quality and spend (same spirit as [08-model-notes.md](./08-model-notes.md)).

Two pipelines:

```
Sentiment:  text → tokenize → embed → classifier → softmax → {neg, neu, pos}
Router:     text → measure complexity → { simple: fast model | complex: crew / first-mate }
```

## Slides & demo

| Demo | Slides | App |
|------|--------|-----|
| Sentiment | [slides](../slides/sentiment/index.html) | [app](../demos/sentiment/app/index.html) |
| Complexity router | [slides](../slides/complexity-router/index.html) | [app](../demos/complexity-router/app/index.html) |

## Related

- [tokenize.md](./tokenize.md), [embedding.md](./embedding.md), [softmax.md](./softmax.md)
- [07-agents.md](./07-agents.md) — crew / first-mate for the complex branch
- Train: [06-train-infer.md](./06-train-infer.md), [train-gpu.md](./train-gpu.md)
