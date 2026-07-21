# Train → Inference

> Mọi mô hình đều sống hai đời: đời **học** (train) tốn công một lần để chỉnh trọng số, và đời **dùng** (inference) chạy đi chạy lại để dự đoán. Hiểu tách bạch hai pha này giúp biết chỗ nào tốn GPU, chỗ nào chạy nhẹ.

## Vì sao quan trọng

Người mới hay gộp "AI" thành một khối. Thực ra phần *nặng* (train nhiều epoch trên GPU) chỉ làm một lần để ra checkpoint; phần *nhẹ* (inference) mới là thứ chạy trong app mỗi lần người dùng bấm. Các demo trong lab đều là inference — train thật diễn ra ở notebook / cloud GPU rồi mới cắm trọng số vào.

## Hai pha

| Pha | Việc | Chi phí | Output |
|-----|------|---------|--------|
| **Train** | Lặp qua dữ liệu nhiều epoch, so dự đoán với đáp án, chỉnh trọng số | Nặng, cần GPU | checkpoint (bộ trọng số) |
| **Inference** | Nạp trọng số, đưa đầu vào, lấy dự đoán | Nhẹ, chạy realtime | nhãn / hành động |

```
data → train (nhiều epoch trên GPU) → checkpoint → load → infer (dự đoán)
```

## Ý chính

- **Học = giảm sai số:** mỗi vòng, mô hình dự đoán, đo lệch (loss, vd cross-entropy đi cùng [softmax.md](./softmax.md)), rồi dịch trọng số theo hướng bớt lệch.
- **Checkpoint là "thành phẩm":** train xong ta cất bộ trọng số; từ đó inference không cần dữ liệu train nữa.
- **Trong AI Lab:** browser demos = minh họa *inference*, không train trong trình duyệt. Train nặng ở notebook protonx / Kaggle / Colab → export → cắm vào UI.

## Related

- Đầy đủ stack (PyTorch, TensorFlow, HF, Kaggle, GPU): [train-gpu.md](./train-gpu.md)
- Demo inference: [04-demo-car.md](./04-demo-car.md), [05-demo-text.md](./05-demo-text.md)
- [softmax.md](./softmax.md) — loss khi train phân loại
