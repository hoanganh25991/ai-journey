# Train · PyTorch / TensorFlow · GPU notebooks

> Where models *actually learn*: data from Hugging Face / Kaggle, code in PyTorch or TensorFlow, many epochs on a GPU (Colab/cloud) until good enough, then export weights.

## Why it matters

Lab demos illustrate inference only. To get a model you can plug in, you must train somewhere with a GPU. This note collects the practical stack — which tools, where data lives, where to run — so you do not rebuild the checklist every time.

## Key ideas

- **Two layers of work:**

  | Layer | Job | Output |
  |-------|-----|--------|
  | **Training** | HF/Kaggle → notebook/endpoint → many GPU epochs | checkpoint |
  | **Inference** | load model → predict | label / action |

  See [06-train-infer.md](./06-train-infer.md) for the two-phase mental model.

- **Stack used in practice:**
  - **PyTorch** — flexible; most training code in the lab.
  - **TensorFlow** — softmax regression and Embedding Projector for visualizing vectors.
  - **Data:** Hugging Face Datasets and Kaggle — pre-labeled, ready to download.
  - **GPU online:** Google Colab / cloud notebooks — train to ~95%+ accuracy, then export.

- **Short workflow:**

  ```
  pick dataset (HF/Kaggle) → write notebook (PyTorch/TF) → train on GPU
  → watch loss/accuracy → export checkpoint → plug into demo (inference)
  ```

- **In AI Lab:** browser demos show the flow; they do **not** replace GPU training. Train in a notebook / Kaggle / Colab, then embed weights in UI demos (car-nn, sentiment…).

## Pipeline

```
HF/Kaggle data → notebook (PyTorch/TF) → GPU epochs → checkpoint → demo inference
```

## References

- [PyTorch — Training a classifier](https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html)
- [Hugging Face Datasets](https://huggingface.co/docs/datasets/)

## Related

- [06-train-infer.md](./06-train-infer.md) — train vs infer
- Demo: [04-demo-car.md](./04-demo-car.md), [05-demo-text.md](./05-demo-text.md), [softmax.md](./softmax.md)
