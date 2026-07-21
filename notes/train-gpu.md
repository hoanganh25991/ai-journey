# Train · PyTorch / TensorFlow · GPU notebooks

Từ `requirement.md` + protonx assignments.

## Hai lớp

| Lớp | Việc | Output |
|-----|------|--------|
| **Training** | HF/Kaggle → notebook/endpoint → epochs trên GPU | checkpoint |
| **Inference** | Load model → predict | label / action |

## Stack đã dùng

- **PyTorch** — classifier, transformer (protonx day-15/18)
- **TensorFlow** — softmax regression, embedding projector
- **Datasets**: Hugging Face, Kaggle
- **GPU online**: Colab-class / cloud IPy notebook — train đến ~95%+ rồi export model

## Protonx code

- `day-15-assignment-train-torch.py`, `day-15-assignment-kaggle-torch.ipynb`
- `day-18-assignment-pytorch-language-detection-transformer*.ipynb`
- `day-8-review-softmax-regression-tensroflow.ipynb`

## Trong AI Lab

Browser demos minh họa flow (không thay GPU train). Train thật ở notebook protonx / Kaggle / Colab → sau đó cắm weights vào UI demo.

## Related

- [sentiment](../demos/sentiment/), [car-nn](../demos/car-nn/), [softmax](../demos/softmax/)
- [06-train-infer.md](./06-train-infer.md)
