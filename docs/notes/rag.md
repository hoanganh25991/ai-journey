# RAG — Retrieval-Augmented Generation

> Thay vì bắt mô hình trả lời bằng mỗi trí nhớ, trước tiên đi *tra cứu* tài liệu liên quan rồi mới để mô hình *soạn* câu trả lời dựa trên đó. Giống mở sách ra tra trước khi phát biểu.

## Vì sao quan trọng

Mô hình ngôn ngữ biết nhiều nhưng hay "chém" (bịa) khi gặp thứ ngoài trí nhớ, và không cập nhật tài liệu riêng của bạn. RAG vá cả hai: neo câu trả lời vào một kho tài liệu thật (tài liệu công ty, video, repo…), kèm trích dẫn nguồn. Nhờ vậy trả lời đúng hơn, cập nhật hơn, và kiểm chứng được — không cần train lại mô hình.

## Ý chính

- **Hai pha:**
  - *Retrieve*: đổi câu hỏi thành vector ([embedding.md](./embedding.md)), tìm trong vector DB ra top-k đoạn (chunk) gần nghĩa nhất.
  - *Generate*: nhét các đoạn đó vào prompt làm ngữ cảnh, mô hình soạn câu trả lời bám theo.
- **Chunk + vector DB:** tài liệu được cắt thành đoạn nhỏ, mỗi đoạn một vector; DB (FAISS, Chroma, pgvector…) lo tìm nhanh đoạn gần nhất, có thể lọc thêm bằng metadata.
- **Khác chat thuần:** chat thuần dựa vào trí nhớ mô hình; RAG luôn *neo vào corpus* nên trả lời được câu về tài liệu mô hình chưa từng thấy.
- **Chất lượng phụ thuộc retrieve:** lấy sai đoạn thì mô hình soạn hay đến mấy cũng sai. Cắt chunk hợp lý và embedding tốt là mấu chốt.
- **Biến thể nâng cao:** *Graph RAG* nối các thực thể thành đồ thị để trả lời câu bắc cầu; rerank, hybrid search (từ khóa + vector) để tăng độ chính xác.

## Hình minh họa

![Embed câu hỏi rồi đi truy vấn kho tài liệu](assets/protonx/embed-then-query.jpg)

![Đường đi của một pipeline RAG](assets/protonx/drop-rag.jpg)

![Graph RAG: nối thực thể thành đồ thị để trả lời câu bắc cầu](assets/protonx/graph-rag.jpg)

![RAG nâng cao: thêm rerank / lọc để tăng độ chính xác](assets/protonx/rag-advanced.jpg)

## Trong pipeline

```
câu hỏi → embed → tìm top-k trong vector DB → (đoạn + câu hỏi) → LLM → trả lời + trích dẫn
```

RAG đứng trên [embedding.md](./embedding.md); Personal Knowledge-base của lab đi đúng hướng này ([personal-knowledge-base.md](./personal-knowledge-base.md)).

## Slides & demo

| | Link |
|--|------|
| Slides | [slides/rag](../slides/rag/index.html) |
| Working app | [demos/rag/app](../demos/rag/app/index.html) |

## Tham khảo

- Lewis et al. 2020 — [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- [Microsoft GraphRAG](https://microsoft.github.io/graphrag/)

## Related

- [vector-database.md](./vector-database.md), [semantic-search.md](./semantic-search.md) — hạ tầng & retrieve cho RAG
- [embedding.md](./embedding.md), [personal-knowledge-base.md](./personal-knowledge-base.md)
