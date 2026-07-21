# Demo: Sentiment & Complexity routing

> Hai demo văn bản dùng chung một ý: đọc một câu rồi *dán nhãn* cho nó. Sentiment dán nhãn cảm xúc; Complexity router dán nhãn "câu này dễ hay khó" để chọn cách xử lý.

## Vì sao đáng xem

Đây là nơi chuỗi khái niệm tokenize → embedding → softmax chạy end-to-end trên câu chữ thật, và cho thấy phân loại không chỉ để "đoán cảm xúc" mà còn để *điều phối* hệ thống: câu dễ thì trả lời nhanh, câu khó mới huy động agent phức tạp.

## Hai pipeline

```
Sentiment:   text → tokenize → embed → classifier → softmax → {neg, neu, pos}
Router:      text → đo độ phức tạp → { đơn giản: model nhanh | phức tạp: crew / first-mate }
```

## Ý chính

- **Sentiment (phân loại cảm xúc):** ba lớp tiêu cực / trung tính / tích cực. Dùng lại đúng chuỗi [tokenize.md](./tokenize.md) → [embedding.md](./embedding.md) → [softmax.md](./softmax.md).
- **Complexity router (định tuyến theo độ khó):** phân loại yêu cầu thành "đơn giản" hay "phức tạp" rồi định tuyến — câu đơn giản đi model nhanh/rẻ, câu phức tạp mới gọi tới crew nhiều agent hoặc first-mate.
- **Cùng một khuôn, khác mục đích:** cả hai đều là bài phân loại; điểm khác là *dùng nhãn để làm gì* — hiển thị cảm xúc, hay quyết định đường đi tiếp theo.
- **Định tuyến = tiết kiệm:** không phải câu nào cũng cần mô hình mạnh nhất; router giúp cân bằng chất lượng và chi phí, cùng tinh thần với [08-model-notes.md](./08-model-notes.md).

## Slides & apps

| Demo | Slides | App |
|------|--------|-----|
| Sentiment | [slides](../slides/sentiment/index.html) | [app](../demos/sentiment/app/index.html) |
| Complexity router | [slides](../slides/complexity-router/index.html) | [app](../demos/complexity-router/app/index.html) |

## Related

- [tokenize.md](./tokenize.md), [embedding.md](./embedding.md), [softmax.md](./softmax.md)
- [07-agents.md](./07-agents.md) — crew / first-mate cho nhánh phức tạp
- Huấn luyện: [06-train-infer.md](./06-train-infer.md), [train-gpu.md](./train-gpu.md)
