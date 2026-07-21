# Train → Inference

> Every model lives two lives: **learning** (train) — spend heavy compute once to adjust weights — and **using** (inference) — run lightly again and again to predict. Knowing the split clarifies what needs a GPU and what runs in the browser. Everyday metaphor: years at school (train) vs answering one exam question (infer).

## Why it matters

Beginners often treat “AI” as one block. Training (many GPU epochs) happens once to produce a checkpoint; inference (predict on new input) is what runs every time a user clicks. Lab demos are all inference — real training happens in notebooks / cloud GPU, then weights plug into the UI.

This mental model prevents two mistakes: (1) expecting a static HTML demo to “learn” from clicks, and (2) renting a GPU for every prediction when a CPU/GPU-light forward pass is enough.

## Key ideas

- **Two phases:**

  | Phase | Work | Cost | Output |
  |-------|------|------|--------|
  | **Train** | loop data for many epochs, compare prediction to label, update weights | heavy, needs GPU | checkpoint (weight file) |
  | **Inference** | load weights, feed input, get prediction | light, realtime | label / action |

  Training needs labels, an optimizer, and many passes over data. Inference needs only the frozen weights and a forward pass — no labels, no `backward()`.

- **Learning = reducing error:** each round the model predicts, measures loss (e.g. cross-entropy with [softmax.md](./softmax.md)), then nudges weights toward lower loss ([pytorch-training.md](./pytorch-training.md)). The update rule is usually SGD/Adam on gradients of that loss. One epoch = one full pass over the training set; “many epochs” means repeating until val metrics plateau.

- **Checkpoint is the product:** after training, save weights; inference no longer needs training data or labels. A checkpoint is the transferable artifact between notebook and demo. Formats you will see: `state_dict` (`.pt`), Keras SavedModel, ONNX, Hugging Face Hub folders.

- **Eval / serve mode:** at inference, disable dropout / use running batch-norm stats (`model.eval()`, `torch.no_grad()`). Training mode keeps dropout noise and updates BN stats — fine while learning, wrong when serving. Always wrap serve paths in no-grad so you do not accidentally build a graph.

- **Fine-tune is still training:** loading a Hub model and updating weights on your labels is a *train* phase (lighter, but still GPU + labels). Calling the resulting API is *inference*. “Chat with the model” without updating weights is inference.

- **In AI Lab:** browser demos show *inference* only. Heavy training in protonx / Kaggle / Colab notebooks → export → embed in UI ([train-gpu.md](./train-gpu.md)). If a demo button feels “smart,” it is running a forward pass on weights you already trained elsewhere.

## Worked example (intuition)

**Car-nn (sensors → drive action):**

1. **Train (notebook):** weeks of GPU loops on labeled sensor → action pairs. Each step: forward → compare to label → loss → backward → update weights. Periodically evaluate on a held-out track; keep the best validation checkpoint as `weights.json` (or `.pt`).
2. **Export:** write the weight tensors into the demo’s static assets. No training data ships with the demo.
3. **Infer (browser):** on “drive,” the UI reads current sensor values, runs one forward pass through the fixed network, and outputs an action (steer / accel). Clicks never call an optimizer — that would be training, and it already happened.
4. **What users feel:** low latency. What you paid once: GPU hours and label collection.

**Sentiment demo (same split):** notebook fine-tunes a classifier → export → each review click is `argmax(softmax(logits))` only. If predictions look random after a deploy, check `eval()` / wrong checkpoint — not “needs more clicks to learn.”

## Common pitfalls

- **Confusing fine-tune with inference** — fine-tune is still training (updates weights).
- **Leaving dropout on at serve time** — noisy, inconsistent predictions.
- **Shipping the last epoch blindly** — prefer the best validation checkpoint.
- **Re-training from scratch when a Hub model + light fine-tune would do**.
- **Renting a GPU for every API call** — most classification forward passes are fine on CPU once the model is small.

## Illustrations

![Train vs Inference: two panels](assets/train-infer/train-infer-split.png)

![Two lives of a model — flow diagram](assets/train-infer/train-infer-flow.svg)

![Training curves vs inference product](assets/train-infer/overfit-curves.png)

## Deeper dive

- **What each phase allocates:** train keeps activations for backward, optimizer states (Adam ≈ 2× params), and data loaders. Infer keeps weights + activations for one batch. That is why train VRAM ≫ serve VRAM for the same architecture.
- **`train()` vs `eval()` is not optional:** dropout and BatchNorm behave differently. Forgetting `eval()` makes the same input yield different outputs across clicks — users blame “the model,” but it is mode.
- **Checkpoint selection policy:** track `val_loss` / `val_f1` every epoch; save when improved; optionally keep top-3. Report metrics from the **chosen** checkpoint, not a cherry-picked mid-run print.
- **Quantization and distillation are inference-side tricks:** they shrink or speed the forward pass after training. They do not replace a good train/val loop; they package a finished model for edge/browser.
- **Online learning ≠ clicking in a demo:** continually updating weights from live traffic is a deliberate training system (labels, monitoring, rollback). Lab demos do not do this.
- **Latency budgets:** train optimizes for final quality; serve optimizes for p95 latency and cost. A 0.5% accuracy gain that triples serve cost may be wrong for a product, fine for a research notebook.
- **Reproducibility bridge:** same tokenizer, same preprocessing, same label map between train and infer. Mismatched class order (`neg/neu/pos` vs `pos/neu/neg`) silently swaps predictions.

## Decision guide

| Situation | Prefer | Avoid / why |
|-----------|--------|-------------|
| User-facing click / API predict | Load checkpoint, `eval()`, forward only | Running epochs or `loss.backward()` in the request path |
| Need better accuracy on your labels | Fine-tune (train phase) on GPU, then re-export | Hoping inference-time prompt tricks replace labeled training for classifiers |
| Demo must run in static HTML | Small frozen weights + JS/ONNX forward | Expecting the page to “learn” from user clicks |
| Predictions flicker with same input | Force `model.eval()` + deterministic seed where relevant | Leaving dropout active at serve |
| Choosing which file to ship | Best validation checkpoint | Last epoch by default — often overfit |
| Cost spike on every prediction | Distill / quantize / smaller model for serve | Renting train-class GPUs for light forward passes |

## Pipeline

```
data → train (many GPU epochs) → checkpoint → load → infer (predict)
```

## Slides & demo

| | Link |
|--|------|
| Slides | [slides/train-infer](../slides/train-infer/index.html) |
| Related demos | [car-nn](../demos/car-nn/app/index.html) · [sentiment](../demos/sentiment/app/index.html) |

## Related

- Full stack (PyTorch, TensorFlow, HF, Kaggle, GPU): [train-gpu.md](./train-gpu.md)
- Demo inference: [04-demo-car.md](./04-demo-car.md), [05-demo-text.md](./05-demo-text.md)
- [softmax.md](./softmax.md) — loss when training classifiers
- [pytorch-training.md](./pytorch-training.md), [tensorflow-training.md](./tensorflow-training.md)
