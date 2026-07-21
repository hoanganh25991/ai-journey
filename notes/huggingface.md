# Hugging Face — dataset + Space → ra model

> "GitHub của AI": nơi lấy sẵn **dataset**, **model** pretrained, và chạy/host demo bằng **Spaces**. Rút ngắn quãng đường từ ý tưởng tới một model dùng được.

## Vì sao quan trọng

Tự train từ đầu rất tốn. Hugging Face cho phép *đứng trên vai người khác*: tải dataset có sẵn, lấy model pretrained rồi chỉ fine-tune nhẹ, và deploy demo trong vài phút. Đây là cách nhanh nhất để đi từ [training](./pytorch-training.md) tới một model có thể chia sẻ.

## Ba mảnh chính

| Mảnh | Là gì | Dùng để |
|------|-------|---------|
| **Datasets** | kho dữ liệu có nhãn, tải 1 dòng `load_dataset(...)` | có ngay dữ liệu train/eval |
| **Models (Hub)** | model pretrained (BERT, GPT, ViT…) | fine-tune thay vì train từ 0 |
| **Spaces** | host app demo (Gradio/Streamlit), có GPU | chạy & chia sẻ model ra web |

## Ý chính

- **`transformers` + `datasets`:** vài dòng là nạp được model + tokenizer + dữ liệu; fine-tune bằng `Trainer` hoặc vòng lặp PyTorch/TF quen thuộc.
- **Fine-tune > train from scratch:** tận dụng kiến thức đã học của model lớn → cần ít dữ liệu và thời gian hơn nhiều.
- **Spaces = demo + endpoint:** đẩy model lên Space (kèm GPU nếu cần) → có ngay UI và API để người khác thử.
- **Model card & license:** đọc kỹ giấy phép và giới hạn trước khi dùng thương mại.
- **Output là một model:** kết quả cuối là checkpoint/endpoint sẵn sàng [inference](./06-train-infer.md).

## Trong pipeline

```
HF Datasets → model pretrained (Hub) → fine-tune (PyTorch/TF) → push lên Hub / Spaces → dùng
```

Hugging Face là "nguồn dữ liệu + nơi chạy" cho [pytorch-training.md](./pytorch-training.md) / [tensorflow-training.md](./tensorflow-training.md); dữ liệu thi đấu thì xem [kaggle.md](./kaggle.md).

## Tham khảo

- [Hugging Face Hub](https://huggingface.co/docs/hub/) · [Datasets](https://huggingface.co/docs/datasets/) · [Spaces](https://huggingface.co/docs/hub/spaces)
- [transformers](https://huggingface.co/docs/transformers/)

## Related

- [pytorch-training.md](./pytorch-training.md), [tensorflow-training.md](./tensorflow-training.md)
- [kaggle.md](./kaggle.md), [sentence-transformers.md](./sentence-transformers.md), [train-gpu.md](./train-gpu.md)
