# Hugging Face — dataset + Space → usable model

> "GitHub for AI": get **datasets**, **pretrained models**, and host demos with **Spaces**. Shortens the path from idea to a model you can actually use.

## Why it matters

Training from scratch is expensive. Hugging Face lets you stand on others' work: download a labeled dataset, grab a pretrained model, fine-tune lightly, and deploy a demo in minutes. It is the fastest route from [training](./pytorch-training.md) to a shareable model.

## Key ideas

- **Three main pieces:**
  - *Datasets* — labeled data, one line: `load_dataset(...)`.
  - *Models (Hub)* — pretrained BERT, GPT, ViT, etc.; fine-tune instead of training from zero.
  - *Spaces* — host demo apps (Gradio/Streamlit), with optional GPU.
- **`transformers` + `datasets`:** a few lines to load model, tokenizer, and data; fine-tune with `Trainer` or a familiar PyTorch/TF loop.
- **Fine-tune beats scratch:** leverage knowledge from large models → needs far less data and time.
- **Spaces = demo + endpoint:** push a model to a Space → instant UI and API for others to try.
- **Model card and license:** read license and usage restrictions before commercial use.
- **Output is a model:** checkpoint or endpoint ready for [inference](./06-train-infer.md).

## Pipeline

```
HF Datasets → pretrained model (Hub) → fine-tune (PyTorch/TF) → push to Hub / Spaces → use
```

Hugging Face is the data source and runtime for [pytorch-training.md](./pytorch-training.md) / [tensorflow-training.md](./tensorflow-training.md); for competition-style data, see [kaggle.md](./kaggle.md).

## References

- [Hugging Face Hub](https://huggingface.co/docs/hub/) · [Datasets](https://huggingface.co/docs/datasets/) · [Spaces](https://huggingface.co/docs/hub/spaces)
- [transformers](https://huggingface.co/docs/transformers/)

## Related

- [pytorch-training.md](./pytorch-training.md), [tensorflow-training.md](./tensorflow-training.md)
- [kaggle.md](./kaggle.md), [sentence-transformers.md](./sentence-transformers.md), [train-gpu.md](./train-gpu.md)
