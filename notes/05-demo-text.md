# Demo: Sentiment & Complexity routing

## Slides & apps

| Demo | Slides | App |
|------|--------|-----|
| Sentiment | [slides](../demos/sentiment/slides/) | [app](../demos/sentiment/app/) |
| Complexity router | [slides](../demos/complexity-router/slides/) | [app](../demos/complexity-router/app/) |

## Pipelines

```
text → tokenize → embed → classifier → {neg, neu, pos}
text → complexity → simple(fast) | complex(crew / first-mate)
```

Train that: PyTorch/TF + HF/Kaggle + GPU — xem [train-gpu.md](./train-gpu.md).

## Related

- [tokenize.md](./tokenize.md), [embedding.md](./embedding.md), [softmax.md](./softmax.md)
- [mcp.md](./mcp.md), [07-agents.md](./07-agents.md)
