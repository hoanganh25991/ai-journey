# Vector database

> Nơi cất hàng triệu vector embedding và trả lời cực nhanh câu hỏi "vector nào gần cái này nhất?". Là hạ tầng đứng dưới RAG và semantic search.

## Vì sao quan trọng

[Embedding](./embedding.md) biến mọi thứ thành vector, nhưng có vector rồi thì cất ở đâu và tìm thế nào? Duyệt lần lượt cả triệu vector để so từng cái (brute-force) thì quá chậm. Vector database giải đúng bài này: lưu vector kèm dữ liệu gốc, và tìm top-k "hàng xóm gần nhất" trong mili-giây nhờ chỉ mục xấp xỉ. Không có nó, [RAG](./rag.md) và [semantic search](./semantic-search.md) không chạy được ở quy mô thật.

## Ý chính

- **Bài toán lõi — nearest neighbor:** cho một vector truy vấn, tìm k vector gần nhất theo cosine / dot-product ([embedding.md](./embedding.md)).
- **ANN thay vì brute-force:** chỉ mục *xấp xỉ* (HNSW, IVF…) đánh đổi một chút độ chính xác để tăng tốc hàng trăm lần — đủ tốt cho tìm kiếm.
- **Không chỉ là vector:** mỗi bản ghi kèm *metadata* (nguồn, ngày, nhãn) để **lọc** trước/sau khi tìm; và cần CRUD (thêm/sửa/xóa) khi dữ liệu thay đổi.
- **Vài lựa chọn quen thuộc:**
  - *FAISS* — in-memory, rất nhanh, hợp thử nghiệm; nhưng thiếu CRUD và lưu bền.
  - *Elasticsearch (kNN plugin)* — tích hợp sẵn với keyword search, có CRUD, phân tán được.
  - *pgvector / Chroma* — gắn thẳng vào Postgres / dùng nhẹ cho app nhỏ.
- **Chọn theo nhu cầu:** cần quy mô + CRUD + phân tán → Elastic; cần tốc độ thuần trong RAM → FAISS.

## Hình minh họa

![Embed câu hỏi rồi đi truy vấn kho vector](assets/protonx/embed-then-query.jpg)

![Khi nào dùng cosine, khi nào dùng dot-product để so vector](assets/protonx/cosine-vs-dot.jpg)

## Trong pipeline

```
tài liệu → chunk → embedding → [vector database]
câu hỏi  → embedding → [vector database: tìm top-k] → RAG / semantic search
```

Vector database nhận vector từ [embedding.md](./embedding.md) và cấp top-k cho [rag.md](./rag.md) lẫn [semantic-search.md](./semantic-search.md).

## Tham khảo

- [FAISS (Meta)](https://github.com/facebookresearch/faiss)
- [pgvector](https://github.com/pgvector/pgvector) · [Elasticsearch kNN search](https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search.html)

## Related

- [embedding.md](./embedding.md), [rag.md](./rag.md), [semantic-search.md](./semantic-search.md)
