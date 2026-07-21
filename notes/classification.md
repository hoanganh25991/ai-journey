# Classification — label the input

> Given an input (text, image, numbers), the model picks one label from a fixed set. This is the most common "build a model" problem — right after [softmax](./softmax.md).

## Why it matters

Much practical work is categorization: is this review positive or negative, is the email spam, is the photo a dog or a cat, is the question easy or hard. Understanding classification is understanding how a model makes discrete decisions — and it reuses the same tokenize → embedding → softmax chain the lab walks through.

## Key ideas

- **Classification head:** the last layer turns a representation (vector) into a score per label (logits), then [softmax](./softmax.md) converts to probabilities → pick the highest.
- **Binary vs multi-class vs multi-label:**
  - *Binary:* two classes (spam / not spam).
  - *Multi-class:* pick exactly one of many (neg / neu / pos).
  - *Multi-label:* one input can carry several labels at once.
- **Training loss:** *cross-entropy* measures how wrong the predicted probability is; training pushes loss down ([06-train-infer.md](./06-train-infer.md)).
- **Evaluation:** accuracy is easy but misleading on imbalanced data; also check precision, recall, and F1.
- **Class balance:** rare labels are easily ignored — watch the label distribution.

## Illustrations

![Softmax regression: multi-class classification model](assets/protonx/softmax-regression.jpg)

![Softmax converts raw scores to probabilities for label selection](assets/protonx/softmax.jpg)

## Pipeline

```
input → embedding → classification head → softmax → label
                                    (train: cross-entropy)
```

Classification is the destination of [softmax.md](./softmax.md); train it with [pytorch-training.md](./pytorch-training.md) or [tensorflow-training.md](./tensorflow-training.md).

## References

- [scikit-learn — classification](https://scikit-learn.org/stable/supervised_learning.html)
- Google — [Classification (ML Crash Course)](https://developers.google.com/machine-learning/crash-course/classification/video-lecture)

## Related

- [softmax.md](./softmax.md), [05-demo-text.md](./05-demo-text.md)
- [pytorch-training.md](./pytorch-training.md), [tensorflow-training.md](./tensorflow-training.md)
