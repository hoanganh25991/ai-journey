# Tokenize

> Máy không đọc chữ — nó đọc số. Tokenize là bước cắt câu chữ thành những mẩu nhỏ (token) rồi đổi mỗi mẩu thành một con số (ID).

## Vì sao quan trọng

Mọi mô hình ngôn ngữ chỉ nhận vào một dãy số. Trước khi làm bất cứ điều gì — embedding, attention, phân loại — câu chữ phải được biến thành dãy ID. Nếu bước cắt này sai, mọi bước sau đều nhận sai đầu vào. Tokenizer vì thế là "cửa khẩu" của cả pipeline.

## Ý chính

- **Ba mức cắt:**
  - *Theo từ* (word): `"xin chào"` → `["xin", "chào"]`. Đơn giản nhưng gặp từ lạ là chịu.
  - *Theo mẩu con* (subword): `"chàoo"` → `["chào", "o"]`. Ghép được từ chưa gặp từ các mẩu đã biết — cách phổ biến nhất hiện nay.
  - *Theo ký tự* (char): `"chào"` → `["c","h","à","o"]`. Không bao giờ bí, nhưng chuỗi rất dài.
- **Vocabulary (từ điển):** tập cố định mọi token mà mô hình biết; mỗi token ứng với một ID. Ví dụ `chào → 5021`.
- **BPE vs WordPiece:** hai cách xây từ điển subword. Cùng ý tưởng "gộp dần cặp hay đi cùng nhau", khác ở tiêu chí gộp. Đây là kiểu tokenizer của GPT (BPE) và BERT (WordPiece).
- **Một token ≈ 4 ký tự tiếng Anh:** nên chi phí gọi mô hình tính theo token, không theo chữ.
- **Sai tokenizer = sai tất cả:** dùng tokenizer khác lúc train và lúc chạy → ID lệch → mô hình hiểu nhầm hoàn toàn.

## Hình minh họa

![Câu chữ được cắt thành các token, mỗi token tô một màu](assets/protonx/tokenizer-viz.jpg)

![BPE và WordPiece: hai cách xây từ điển subword](assets/protonx/bpe-vs-wordpiece.png)

![Gộp dần các cặp ký tự hay đi cùng nhau để dựng vocabulary](assets/protonx/build-vocab.jpg)

## Trong pipeline

```
văn bản → [tokenize] → IDs → embedding → attention → … → softmax
```

Token ID là đầu vào cho [embedding.md](./embedding.md); từ đó mới tới attention, phân loại, RAG.

## Slides & demo

| | Link |
|--|------|
| Slides | [slides/tokenize](../slides/tokenize/index.html) |
| Working app | [demos/tokenize/app](../demos/tokenize/app/index.html) |

## Tham khảo

- Hugging Face — [Tokenizers summary](https://huggingface.co/docs/transformers/tokenizer_summary)
- Sennrich et al. 2016 — [Neural Machine Translation of Rare Words with Subword Units (BPE)](https://arxiv.org/abs/1508.07909)

## Related

- [embedding.md](./embedding.md), [05-demo-text.md](./05-demo-text.md)
