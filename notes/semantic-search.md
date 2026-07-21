# Semantic search — hybrid · tiered · fallback

> Tìm theo *nghĩa* chứ không chỉ khớp từ khóa, bằng cách ghép hai loại chỉ mục: inverted index (Elastic, theo từ khóa) và semantic index (embedding, theo nghĩa). Đây là dự án mình làm để học sâu về RAG.

> Repo: [github.com/hoanganh25991/semantic-search](https://github.com/hoanganh25991/semantic-search) — Hybrid / Tiered / Fallback trên dataset MS MARCO.

## Vì sao quan trọng

Tìm bằng từ khóa (BM25 / TF-IDF trong Elastic) thì nhanh và rẻ, nhưng "xe hơi" với "ô tô" là hai từ khác nhau nên dễ trượt. Tìm bằng [embedding](./embedding.md) thì hiểu nghĩa, nhưng nặng và tốn khi chạy trên mọi câu. Semantic search thực dụng là **kết hợp** cả hai: lấy cái nhanh để lọc, cái hiểu nghĩa để xếp hạng. Đây cũng chính là bước "retrieve" chất lượng cao cho [RAG](./rag.md).

## Hai loại chỉ mục

| Chỉ mục | Cơ chế | Mạnh | Yếu |
|---------|--------|------|-----|
| **Inverted index** (Elastic) | map từ khóa → tài liệu | nhanh, rẻ, chính xác với truy vấn rõ | không hiểu từ đồng nghĩa |
| **Semantic index** (embedding) | vector trong [vector database](./vector-database.md) | hiểu nghĩa, bắt được diễn đạt khác | nặng hơn, cần model |

## Ba chiến lược tìm kiếm

- **Hybrid:** dùng inverted index *lọc nhanh* ứng viên theo từ khóa, rồi semantic index *rerank* theo nghĩa. Tối ưu chi phí; điểm yếu là nếu keyword trượt thì thiếu ứng viên để rerank.
- **Tiered:** *phân loại câu hỏi* dễ/khó trước → câu dễ đi keyword, câu khó mới đi semantic. Cân bằng tốc độ và độ chính xác (cùng ý tưởng với [complexity router](./05-demo-text.md)).
- **Fallback:** semantic trước để tối đa độ chính xác, nếu kết quả kém thì *rớt về* keyword. Chính xác cao nhưng đắt hơn.

## Dataset & đánh giá

- **MS MARCO** — câu hỏi thật của người dùng + đoạn văn liên quan, dùng làm testbed.
- **Metrics:** *Precision@k* (tỉ lệ kết quả đúng trong top-k), *MRR@10* (vị trí kết quả đúng đầu tiên) — quan trọng khi câu trả lời đầu tiên là thứ đáng giá nhất.
- **Query classification:** phân loại câu hỏi *simple* (`description`) vs *complex* (`entity`, `location`, `numeric`…) bằng một classifier fine-tune trên embedding — đầu vào cho chiến lược Tiered.

## Kiến trúc lưu trữ

- **MongoDB** — lưu tài liệu thô.
- **Elasticsearch** — lưu dữ liệu đã index (cả inverted lẫn kNN) để tìm nhanh.

## Hình minh họa

![Embed câu hỏi rồi đi truy vấn — bước retrieve của semantic search](assets/protonx/embed-then-query.jpg)

![Retrieval nâng cao: kết hợp lọc + rerank để tăng độ chính xác](assets/protonx/rag-advanced.jpg)

## Trong pipeline

```
câu hỏi → (phân loại dễ/khó) → { keyword: inverted index | nghĩa: semantic index }
        → hợp nhất / rerank → top-k → RAG
```

Semantic search đứng trên [embedding.md](./embedding.md) + [vector-database.md](./vector-database.md), và là bước retrieve cho [rag.md](./rag.md).

## Tham khảo

- Repo: [hoanganh25991/semantic-search](https://github.com/hoanganh25991/semantic-search)
- [MS MARCO](https://microsoft.github.io/msmarco/) · [Elasticsearch kNN](https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search.html)

## Related

- [vector-database.md](./vector-database.md), [rag.md](./rag.md), [embedding.md](./embedding.md)
- [05-demo-text.md](./05-demo-text.md) — complexity router (cùng ý "tiered")
