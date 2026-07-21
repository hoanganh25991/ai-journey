# Train → Inference

> Every model lives two lives: **learning** (train) — spend heavy compute once to adjust weights — and **using** (inference) — run lightly again and again to predict. Knowing the split clarifies what needs a GPU and what runs in the browser.

## Why it matters

Beginners often treat "AI" as one block. Training (many GPU epochs) happens once to produce a checkpoint; inference (predict on new input) is what runs every time a user clicks. Lab demos are all inference — real training happens in notebooks / cloud GPU, then weights plug into the UI.

## Key ideas

- **Two phases:**

  | Phase | Work | Cost | Output |
  |-------|------|------|--------|
  | **Train** | loop data for many epochs, compare prediction to label, update weights | heavy, needs GPU | checkpoint (weight file) |
  | **Inference** | load weights, feed input, get prediction | light, realtime | label / action |

- **Learning = reducing error:** each round the model predicts, measures loss (e.g. cross-entropy with [softmax.md](./softmax.md)), then nudges weights toward lower loss.
- **Checkpoint is the product:** after training, save weights; inference no longer needs training data.
- **In AI Lab:** browser demos show *inference* only. Heavy training in protonx / Kaggle / Colab notebooks → export → embed in UI.

## Pipeline

```
data → train (many GPU epochs) → checkpoint → load → infer (predict)
```

## Related

- Full stack (PyTorch, TensorFlow, HF, Kaggle, GPU): [train-gpu.md](./train-gpu.md)
- Demo inference: [04-demo-car.md](./04-demo-car.md), [05-demo-text.md](./05-demo-text.md)
- [softmax.md](./softmax.md) — loss when training classifiers
