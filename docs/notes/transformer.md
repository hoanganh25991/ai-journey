# Transformer — kiến trúc lõi của LLM

> Kiến trúc ghép nhiều khối [attention](./attention.md) lại, xử lý cả câu song song thay vì tuần tự. Là bộ khung đứng sau BERT, GPT và gần như mọi model ngôn ngữ hiện đại.

## Vì sao quan trọng

Trước Transformer, model đọc câu tuần tự (RNN/LSTM) — chậm và hay quên phần đầu câu. Transformer (2017, "Attention Is All You Need") bỏ tuần tự, cho mọi từ nhìn nhau cùng lúc bằng attention → train nhanh trên GPU và bắt được quan hệ xa. Đây là bước ngoặt mở ra kỷ nguyên LLM.

## Ý chính

- **Xếp chồng khối attention:** mỗi lớp gồm multi-head [attention](./attention.md) + mạng feed-forward, chồng nhiều lớp để học biểu diễn ngày càng trừu tượng.
- **Positional encoding:** vì xử lý song song (không theo thứ tự), phải *chèn thông tin vị trí* để model biết từ nào đứng trước/sau.
- **Encoder / decoder:**
  - *Encoder* (BERT): đọc-hiểu cả câu → hợp cho [classification](./classification.md), embedding.
  - *Decoder* (GPT): sinh từ trái sang phải → hợp cho tạo văn bản.
  - *Encoder-decoder*: dịch máy, tóm tắt (dùng cross-attention).
- **Residual + layer norm:** mẹo giúp mạng sâu vẫn train ổn định.
- **Song song = nhanh:** không phụ thuộc bước trước → tận dụng GPU tối đa ([train-gpu.md](./train-gpu.md)).

## Hình minh họa

![Self-attention trong một khối encoder](assets/protonx/self-attention.jpg)

![Cross-attention: decoder nhìn sang encoder (dịch máy)](assets/protonx/cross-attention.jpg)

![Trọng số attention sau softmax bên trong một lớp](assets/protonx/attention-after-softmax.jpg)

## Trong pipeline

```
tokens → embedding + positional → [N × (multi-head attention + feed-forward)] → biểu diễn
       → head: classification / generation
```

Transformer là "khung nhà" gói [attention.md](./attention.md), [embedding.md](./embedding.md) và [softmax.md](./softmax.md) lại thành một model hoàn chỉnh.

## Tham khảo

- Vaswani et al. 2017 — [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- Jay Alammar — [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)

## Related

- [attention.md](./attention.md), [embedding.md](./embedding.md), [softmax.md](./softmax.md)
- [huggingface.md](./huggingface.md) — model Transformer pretrained
