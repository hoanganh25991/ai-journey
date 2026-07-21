# Transformer — core architecture of LLMs

> Stack many [attention](./attention.md) blocks and process a whole sentence in parallel instead of step by step. The framework behind BERT, GPT, and nearly every modern language model.

## Why it matters

Before Transformers, models read sentences sequentially (RNN/LSTM) — slow and prone to forgetting early context. The Transformer (2017, "Attention Is All You Need") drops sequential processing: every word attends to every other word at once → faster GPU training and better long-range links. That pivot opened the LLM era.

## Key ideas

- **Stacked attention blocks:** each layer has multi-head [attention](./attention.md) plus a feed-forward network; stack many layers for increasingly abstract representations.
- **Positional encoding:** parallel processing has no built-in order — inject position info so the model knows word sequence.
- **Encoder / decoder:**
  - *Encoder* (BERT): read and understand the whole sentence → good for [classification](./classification.md) and embeddings.
  - *Decoder* (GPT): generate left to right → good for text generation.
  - *Encoder-decoder:* translation, summarization (uses cross-attention).
- **Residual + layer norm:** tricks that keep deep networks stable during training.
- **Parallel = fast:** no step-by-step dependency → full GPU utilization ([train-gpu.md](./train-gpu.md)).

## Illustrations

![Self-attention inside one encoder block](assets/protonx/self-attention.jpg)

![Cross-attention: decoder attends to encoder (machine translation)](assets/protonx/cross-attention.jpg)

![Attention weights after softmax inside one layer](assets/protonx/attention-after-softmax.jpg)

## Pipeline

```
tokens → embedding + positional → [N × (multi-head attention + feed-forward)] → representation
       → head: classification / generation
```

The Transformer is the "house frame" wrapping [attention.md](./attention.md), [embedding.md](./embedding.md), and [softmax.md](./softmax.md) into one complete model.

## References

- Vaswani et al. 2017 — [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- Jay Alammar — [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)

## Related

- [attention.md](./attention.md), [embedding.md](./embedding.md), [softmax.md](./softmax.md)
- [huggingface.md](./huggingface.md) — pretrained Transformer models
