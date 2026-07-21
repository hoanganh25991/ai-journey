# Softmax

> Biến một dãy điểm số thô (logits) thành phần trăm: mỗi lựa chọn một xác suất, cộng tất cả lại bằng 1.

## Vì sao quan trọng

Mô hình thường xuất ra vài con số thô, ví dụ điểm cho ba lớp cảm xúc: `tiêu cực 2.0, trung tính 1.0, tích cực 0.1`. Những số này khó đọc và không phải xác suất. Softmax nén chúng thành `[0.66, 0.24, 0.10]` — vừa dễ hiểu ("66% là tiêu cực"), vừa cộng lại bằng 1. Đây là bước cuối ở hầu hết bài phân loại, và cũng là bước chuẩn hóa trọng số bên trong attention.

## Ý chính

- **Công thức trực giác:** lấy `e^điểm` cho từng lựa chọn rồi chia cho tổng. Mũ hóa làm điểm cao nổi bật hơn, điểm thấp bị ép nhỏ lại.
- **Giữ thứ hạng, nới khoảng cách:** lựa chọn điểm cao nhất vẫn xác suất cao nhất, nhưng chênh lệch bị "kéo giãn" — thường ra một đỉnh rõ ràng.
- **Hai chỗ hay gặp:**
  - *Đầu phân loại (classification head)*: ví dụ 3 lớp cảm xúc, xem [05-demo-text.md](./05-demo-text.md).
  - *Trọng số attention*: chuẩn hóa điểm liên quan giữa các từ, xem [attention.md](./attention.md).
- **Đi cặp với cross-entropy khi train:** softmax cho xác suất dự đoán, cross-entropy đo nó lệch bao nhiêu so với đáp án đúng → tín hiệu để mô hình học.
- **Softmax regression = hồi quy logistic nhiều lớp:** phiên bản mở rộng cho bài chọn 1 trong nhiều lớp.

## Hình minh họa

![Softmax biến điểm thô thành phân phối xác suất cộng bằng 1](assets/protonx/softmax.jpg)

![Softmax regression: phân loại nhiều lớp](assets/protonx/softmax-regression.jpg)

## Trong pipeline

```
logits (điểm thô) → [softmax] → xác suất → chọn lớp / trọng số attention
```

Softmax là bước chốt của [05-demo-text.md](./05-demo-text.md) và bước chuẩn hóa bên trong [attention.md](./attention.md).

## Slides & demo

| | Link |
|--|------|
| Slides | [slides/softmax](../slides/softmax/index.html) |
| Working app | [demos/softmax/app](../demos/softmax/app/index.html) |

## Tham khảo

- Google — [ML Crash Course: Softmax](https://developers.google.com/machine-learning/crash-course/multi-class-neural-networks/softmax)
- [CS231n — Softmax classifier](https://cs231n.github.io/linear-classify/#softmax)

## Related

- [classification.md](./classification.md) — bài build model ngay sau softmax
- [attention.md](./attention.md), [05-demo-text.md](./05-demo-text.md)
