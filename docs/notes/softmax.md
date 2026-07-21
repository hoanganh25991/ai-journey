# Softmax

> Turn raw scores (logits) into percentages: each choice gets a probability, and they all add up to 1.

## Why it matters

A model often outputs rough numbers — for three sentiment classes: `negative 2.0, neutral 1.0, positive 0.1`. Those are hard to read and not probabilities. Softmax compresses them to `[0.66, 0.24, 0.10]` — easy to interpret ("66% negative") and guaranteed to sum to 1. It is the final step in most classification tasks and the normalization step inside attention.

## Key ideas

- **Intuitive formula:** take `e^score` for each choice and divide by the total. Exponentiation makes high scores stand out and low scores shrink.
- **Ranking preserved, gap widened:** the highest score still wins, but the spread is stretched — often showing a clear peak.
- **Two common uses:**
  - *Classification head:* e.g. three emotion classes — see [05-demo-text.md](./05-demo-text.md).
  - *Attention weights:* normalize relevance scores between words — see [attention.md](./attention.md).
- **Paired with cross-entropy in training:** softmax gives predicted probabilities; cross-entropy measures how far they are from the correct label → the learning signal.
- **Softmax regression = multi-class logistic regression:** the natural extension when picking one label from many classes.

## Illustrations

![Softmax turns raw scores into a probability distribution that sums to 1](assets/protonx/softmax.jpg)

![Softmax regression: multi-class classification](assets/protonx/softmax-regression.jpg)

## Pipeline

```
logits (raw scores) → [softmax] → probabilities → pick class / attention weights
```

Softmax is the key step in [05-demo-text.md](./05-demo-text.md) and the normalization step inside [attention.md](./attention.md).

## Slides & demo

| | Link |
|--|------|
| Slides | [slides/softmax](../slides/softmax/index.html) |
| Working app | [demos/softmax/app](../demos/softmax/app/index.html) |

## References

- Google — [ML Crash Course: Softmax](https://developers.google.com/machine-learning/crash-course/multi-class-neural-networks/softmax)
- [CS231n — Softmax classifier](https://cs231n.github.io/linear-classify/#softmax)

## Related

- [classification.md](./classification.md) — model building right after softmax
- [attention.md](./attention.md), [05-demo-text.md](./05-demo-text.md)
