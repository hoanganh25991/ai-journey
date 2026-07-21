# Train · PyTorch / TensorFlow · GPU notebooks

> Where models *actually learn*: data from Hugging Face / Kaggle, code in PyTorch or TensorFlow, many epochs on a GPU (Colab/cloud) until good enough, then export weights. Everyday metaphor: the gym (GPU) is where muscles (weights) grow; the phone app (browser demo) only shows the flex.

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
  - **PyTorch** — flexible; most training code in the lab ([pytorch-training.md](./pytorch-training.md)).
  - **TensorFlow** — softmax regression and Embedding Projector for visualizing vectors ([tensorflow-training.md](./tensorflow-training.md)).
  - **Data:** Hugging Face Datasets and Kaggle — pre-labeled, ready to download.
  - **GPU online:** Google Colab / Kaggle / cloud notebooks — train to ~95%+ accuracy when the task allows, then export.

- **Short workflow:**

  ```
  pick dataset (HF/Kaggle) → write notebook (PyTorch/TF) → train on GPU
  → watch loss/accuracy (and val!) → export checkpoint → plug into demo (inference)
  ```

- **In AI Lab:** browser demos show the flow; they do **not** replace GPU training. Train in a notebook / Kaggle / Colab, then embed weights in UI demos (car-nn, sentiment…).

- **What “good enough” means:** for teaching demos, stable val accuracy and sane confusion matrix beat chasing 0.1% leaderboard gains.

## Worked example (intuition)

Sentiment three-class task: download a Hub dataset → fine-tune MiniLM or a small classifier in a Kaggle GPU notebook for a few epochs → export `state_dict` → load in the sentiment demo for live inference. Users never wait for training; you already paid that cost once.

## Common pitfalls

- **Training in the browser demo** — demos are for inference; don’t expect on-device epoch loops.
- **No validation split** — you ship an overfit checkpoint.
- **Forgetting to export** — notebook session ends, weights gone.
- **GPU quota waste** — debug shapes on CPU/small data first.

## Illustrations

![GPU training stack: data → GPU epochs → checkpoint](assets/train-gpu/train-gpu-stack.png)

![Train vs inference split](assets/train-gpu/train-infer-split.png)

## Pipeline

```
HF/Kaggle data → notebook (PyTorch/TF) → GPU epochs → checkpoint → demo inference
```

## Slides & demo

| | Link |
|--|------|
| Slides | [slides/train-gpu](../slides/train-gpu/index.html) |
| Related demos | [car-nn](../demos/car-nn/app/index.html) · [sentiment](../demos/sentiment/app/index.html) |

## References

- [PyTorch — Training a classifier](https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html)
- [Hugging Face Datasets](https://huggingface.co/docs/datasets/)

## Related

- [06-train-infer.md](./06-train-infer.md) — train vs infer
- [pytorch-training.md](./pytorch-training.md), [tensorflow-training.md](./tensorflow-training.md), [huggingface.md](./huggingface.md), [kaggle.md](./kaggle.md)
- Demo notes: [04-demo-car.md](./04-demo-car.md), [05-demo-text.md](./05-demo-text.md)
