# Kaggle — free dataset + notebook + GPU

> ML learning and competition platform: huge **dataset** library, **notebooks** with free **GPU/TPU**, and **competitions** to practice. Similar to Hugging Face but tilted toward hands-on work and leaderboards. Everyday metaphor: a shared workshop with free tools, wood piles (datasets), and contests on the wall.

## Why it matters

When learning, two things are often missing: *good data* and *enough compute*. Kaggle offers both for free — diverse datasets and GPU notebooks in the browser. Competitions add leaderboards and public solutions so you can learn from what top performers do.

Pair it with [Hugging Face](./huggingface.md): grab a pretrained model from the Hub, train on Kaggle’s GPU, export the checkpoint into a lab demo.

## Key ideas

- **Datasets:** tens of thousands of public datasets, downloadable straight into a notebook (or via the Kaggle API).
- **Notebooks (Kernels):** built-in libraries (PyTorch, TF, sklearn…); enable GPU/TPU in settings → train without installing CUDA locally.
- **Competitions:** real problem + metric + leaderboard; submit predictions for a score. Read *public notebooks* for tips — reproducing a strong baseline teaches faster than starting blank.
- **Quota limits:** free GPU hours are capped per week — save them for real training runs, not idle kernels left open overnight.
- **HF connection:** often download data on Kaggle, grab a pretrained model from Hugging Face, then train in a Kaggle notebook.
- **Export:** download weights / ONNX / TorchScript → plug into [inference](./06-train-infer.md) demos (car-nn, sentiment…).

## Short workflow

```
pick dataset (or competition) → new notebook → enable GPU
→ load data + HF model → train epochs → watch val metric
→ export checkpoint → use in demo / Space
```

## Worked example (intuition)

Competition: classify dog breeds from images. You fork a public EfficientNet notebook, swap in a Hub vision model, train 5 epochs on GPU, submit. Leaderboard feedback tells you if augmentation or LR was the real lever — not just “I trained something.”

## Common pitfalls

- **Burning GPU quota on print-debug loops** — debug on CPU / tiny samples first.
- **Ignoring the competition metric** — optimizing accuracy when the score is log-loss.
- **Copy-paste without understanding** — public notebooks win until the private leaderboard; learn *why* steps exist.
- **No offline export plan** — notebook dies with the session; save artifacts to Kaggle datasets or download them.

## Illustrations

![Kaggle stack: dataset → notebook → free GPU](assets/kaggle/kaggle-stack.png)

![Competition loop: train, submit, learn](assets/kaggle/kaggle-loop.png)

## Pipeline

```
Kaggle dataset → notebook (enable GPU) → train (epochs) → export model → inference
```

Same role as “data + GPU runtime” alongside [huggingface.md](./huggingface.md); stack overview at [train-gpu.md](./train-gpu.md).

## Slides & demo

| | Link |
|--|------|
| Slides | [slides/kaggle](../slides/kaggle/index.html) |

## References

- [Kaggle Datasets](https://www.kaggle.com/datasets) · [Notebooks](https://www.kaggle.com/code)
- [Kaggle Learn](https://www.kaggle.com/learn)

## Related

- [huggingface.md](./huggingface.md), [pytorch-training.md](./pytorch-training.md)
- [train-gpu.md](./train-gpu.md), [06-train-infer.md](./06-train-infer.md)
