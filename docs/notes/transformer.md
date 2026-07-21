# Transformer — core architecture of LLMs

> Stack many [attention](./attention.md) blocks and process a whole sentence in parallel instead of step by step. The framework behind BERT, GPT, and nearly every modern language model. Everyday metaphor: instead of reading word-by-word with a bookmark, every word glances at every other word at once — then you deepen that glance across many floors of the building.

## Why it matters

Before Transformers, models read sentences sequentially (RNN/LSTM) — slow and prone to forgetting early context. The Transformer (2017, “Attention Is All You Need”) drops sequential processing: every word attends to every other word at once → faster GPU training and better long-range links. That pivot opened the LLM era.

Everything in this lab that feels “modern” — chat models, embeddings from BERT-like encoders, cross-attention in translation — sits inside this frame.

## Key ideas

- **Stacked attention blocks:** each layer has multi-head [attention](./attention.md) plus a feed-forward network; stack many layers for increasingly abstract representations (syntax → entities → discourse).
- **Positional encoding:** parallel processing has no built-in order — inject position info (sinusoidal or learned) so the model knows word sequence. Without it, “dog bites man” ≈ “man bites dog.”
- **Encoder / decoder / both:**
  - *Encoder* (BERT): read and understand the whole sentence → good for [classification](./classification.md) and embeddings.
  - *Decoder* (GPT): generate left to right with causal masking → good for text generation.
  - *Encoder-decoder:* translation, summarization (uses [cross-attention](./attention.md)).
- **Residual + layer norm:** skip connections and normalization keep deep stacks stable during training.
- **Multi-head = parallel views:** one head may track grammar, another coreference — outputs concatenate and project.
- **Parallel = fast:** no step-by-step dependency → full GPU utilization ([train-gpu.md](./train-gpu.md)).

## Worked example (intuition)

Sentence: `"The cat sat on the mat."`

1. Tokens → embeddings + positional encodings.
2. Layer 1 self-attention: `"sat"` strongly attends to `"cat"` (subject) and `"mat"` (location).
3. Feed-forward mixes features per position.
4. After N layers, a classification head (BERT-style) or next-token head (GPT-style) reads the representation.

## Common pitfalls

- **Confusing encoder vs decoder tasks** — don’t expect a pure encoder to generate fluent chat; don’t expect a causal decoder to be the best frozen sentence embedder without pooling tricks.
- **Ignoring context length** — attention is O(n²) in sequence length; long docs need chunking or efficient variants.
- **Dropping positional info when hacking** — broken order sensitivity.

## Illustrations

![Self-attention inside one encoder block](assets/protonx/self-attention.jpg)

![Cross-attention: decoder attends to encoder (machine translation)](assets/protonx/cross-attention.jpg)

![Attention weights after softmax inside one layer](assets/protonx/attention-after-softmax.jpg)

![Transformer stack: attention + feed-forward layers](assets/transformer/transformer-stack.png)


![Encoder block internals: attention + residual + FFN](assets/transformer/transformer-block-detail.png)

## Pipeline

```
tokens → embedding + positional → [N × (multi-head attention + feed-forward)] → representation
       → head: classification / generation
```

The Transformer is the “house frame” wrapping [attention.md](./attention.md), [embedding.md](./embedding.md), and [softmax.md](./softmax.md) into one complete model.

## Slides & demo

| | Link |
|--|------|
| Slides | [slides/transformer](../slides/transformer/index.html) |
| Related demo | [demos/attention](../demos/attention/app/index.html) |

## References

- Vaswani et al. 2017 — [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- Jay Alammar — [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)

## Related

- [attention.md](./attention.md), [embedding.md](./embedding.md), [softmax.md](./softmax.md)
- [huggingface.md](./huggingface.md) — pretrained Transformer models
