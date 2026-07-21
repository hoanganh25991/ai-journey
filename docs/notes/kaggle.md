# Kaggle — free dataset + notebook + GPU

> ML learning and competition platform: huge **dataset** library, **notebooks** with free **GPU/TPU**, and **competitions** to practice. Similar to Hugging Face but tilted toward hands-on work and leaderboards.

## Why it matters

When learning, two things are often missing: *good data* and *enough compute*. Kaggle offers both for free — diverse datasets and GPU notebooks in the browser. Competitions add leaderboards and public solutions so you can learn from what top performers do.

## Key ideas

- **Datasets:** tens of thousands of public datasets, downloadable straight into a notebook.
- **Notebooks (Kernels):** built-in libraries; enable GPU/TPU in settings → train without installing anything locally.
- **Competitions:** real problem + metric + leaderboard; submit predictions for a score. Read *public notebooks* for tips.
- **Quota limits:** free GPU hours are capped per week — save them for real training runs.
- **HF connection:** often download data on Kaggle, grab a pretrained model from [Hugging Face](./huggingface.md), then train in a Kaggle notebook.

## Pipeline

```
Kaggle dataset → notebook (enable GPU) → train (epochs) → export model → inference
```

Same role as "data + GPU runtime" alongside [huggingface.md](./huggingface.md); stack overview at [train-gpu.md](./train-gpu.md).

## References

- [Kaggle Datasets](https://www.kaggle.com/datasets) · [Notebooks](https://www.kaggle.com/code)
- [Kaggle Learn](https://www.kaggle.com/learn)

## Related

- [huggingface.md](./huggingface.md), [pytorch-training.md](./pytorch-training.md)
- [train-gpu.md](./train-gpu.md), [06-train-infer.md](./06-train-infer.md)
