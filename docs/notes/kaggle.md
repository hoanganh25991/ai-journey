# Kaggle — dataset + notebook + GPU miễn phí

> Nền tảng học và thi đấu ML: kho **dataset** khổng lồ, **notebook** chạy sẵn có **GPU/TPU miễn phí**, và các **competition** để cọ xát. Tương tự Hugging Face nhưng nghiêng về thực hành và thi đấu.

## Vì sao quan trọng

Khi mới học, hai thứ hay thiếu là *dữ liệu tốt* và *máy đủ mạnh*. Kaggle cho cả hai miễn phí: dataset đa dạng và notebook có GPU để train ngay trên trình duyệt. Các competition còn cho leaderboard và lời giải công khai — học từ cách người giỏi làm.

## Ý chính

- **Datasets:** hàng chục nghìn bộ dữ liệu công khai, tải thẳng vào notebook.
- **Notebooks (Kernels):** môi trường chạy sẵn thư viện, bật GPU/TPU trong settings → train không cần cài gì máy cá nhân.
- **Competitions:** đề bài thật + metric + leaderboard; nộp dự đoán để chấm điểm. Đọc *public notebooks* để học mẹo.
- **Giới hạn quota:** GPU miễn phí có hạn giờ/tuần → canh dùng cho lúc train thật.
- **Kết nối HF:** thường tải dataset ở Kaggle, model pretrained ở [Hugging Face](./huggingface.md), rồi train trên notebook Kaggle.

## Trong pipeline

```
Kaggle dataset → notebook (bật GPU) → train (epochs) → export model → inference
```

Cùng vai "dữ liệu + nơi chạy GPU" với [huggingface.md](./huggingface.md); tổng quan stack ở [train-gpu.md](./train-gpu.md).

## Tham khảo

- [Kaggle Datasets](https://www.kaggle.com/datasets) · [Notebooks](https://www.kaggle.com/code)
- [Kaggle Learn](https://www.kaggle.com/learn)

## Related

- [huggingface.md](./huggingface.md), [pytorch-training.md](./pytorch-training.md)
- [train-gpu.md](./train-gpu.md), [06-train-infer.md](./06-train-infer.md)
