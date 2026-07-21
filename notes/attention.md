# Attention

> When reading a word, which other words should you look at to understand it correctly? Attention is how the model decides that for itself.

## Why it matters

In "the dog chased the cat because it was hungry," what does "it" refer to? A reader links "it" to "dog." Attention lets each word scan the whole sentence and assign its own weights: relevant words get high attention; irrelevant ones fade out. That is the core idea behind the Transformer — the architecture behind nearly every modern language model.

## Key ideas

- **Q, K, V — three roles per word:**
  - *Query (Q):* "What information do I need?"
  - *Key (K):* "What information can I provide?"
  - *Value (V):* "The content I actually carry."
  - Compare this word's Q to every word's K → relevance scores → mix V values by those scores.
- **Score → softmax → weighted average:** raw scores pass through [softmax.md](./softmax.md) into weights that sum to 1, then combine V vectors.
- **Self-attention vs cross-attention:** self = words in the *same* sentence look at each other; cross = one sentence attends to another (e.g. translation: target attends to source).
- **Multi-head = parallel views:** one head may capture grammar, another topic — then results merge.

## Illustrations

![Self-attention: each word in a sentence attends to the others](assets/protonx/self-attention.jpg)

![Attention table: weights between every pair of words](assets/protonx/attention-table.jpg)

![Cross-attention: target sentence attends to source sentence](assets/protonx/cross-attention.jpg)

![Attention weights after softmax (sum to 1)](assets/protonx/attention-after-softmax.jpg)

## Pipeline

```
vectors (embedding) → [attention: Q·K → softmax → ×V] → context-rich representation
```

Attention follows [embedding.md](./embedding.md) and uses [softmax.md](./softmax.md) to normalize weights.

## Slides & demo

| | Link |
|--|------|
| Slides | [slides/attention](../slides/attention/index.html) |
| Working app | [demos/attention/app](../demos/attention/app/index.html) |

## References

- Vaswani et al. 2017 — [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- Jay Alammar — [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)

## Related

- [softmax.md](./softmax.md), [embedding.md](./embedding.md)
