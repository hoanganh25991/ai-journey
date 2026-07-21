# Train · PyTorch / TensorFlow · GPU notebooks

> Chỗ để mô hình *thật sự học*: dữ liệu từ Hugging Face / Kaggle, code bằng PyTorch hoặc TensorFlow, chạy nhiều epoch trên GPU (Colab/cloud) đến khi đủ tốt rồi export trọng số.

## Vì sao quan trọng

Demo trong lab chỉ minh họa inference. Muốn có mô hình để cắm vào, phải train ở đâu đó có GPU. Note này gom lại stack thực tế đã dùng — công cụ nào, dữ liệu ở đâu, chạy ở đâu — để không phải nhớ lại mỗi lần bắt đầu một mô hình mới.

## Hai lớp việc

| Lớp | Việc | Output |
|-----|------|--------|
| **Training** | HF/Kaggle → notebook/endpoint → nhiều epoch trên GPU | checkpoint |
| **Inference** | Nạp model → predict | nhãn / hành động |

Khái niệm hai pha xem [06-train-infer.md](./06-train-infer.md).

## Stack đã dùng

- **PyTorch** — linh hoạt, hợp classifier và transformer; phần lớn code train trong lab.
- **TensorFlow** — softmax regression, và Embedding Projector để nhìn vector.
- **Dữ liệu:** Hugging Face Datasets và Kaggle — tải sẵn, có sẵn nhãn.
- **GPU online:** Google Colab / cloud notebook — train tới ~95%+ rồi export model.

## Quy trình gọn

```
chọn dataset (HF/Kaggle) → viết notebook (PyTorch/TF) → train trên GPU
→ theo dõi loss/accuracy → export checkpoint → cắm vào demo (inference)
```

## Trong AI Lab

Browser demos minh họa flow, **không** thay GPU train. Train thật ở notebook / Kaggle / Colab; sau đó lấy weights nhúng vào UI demo (car-nn, sentiment…).

## Tham khảo

- [PyTorch — Training a classifier](https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html)
- [Hugging Face Datasets](https://huggingface.co/docs/datasets/)

## Related

- [06-train-infer.md](./06-train-infer.md) — hai pha train/infer
- Demo: [04-demo-car.md](./04-demo-car.md), [05-demo-text.md](./05-demo-text.md), [softmax.md](./softmax.md)
