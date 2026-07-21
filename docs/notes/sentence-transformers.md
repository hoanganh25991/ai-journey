# sentence-transformers — embedding câu trong vài dòng

> Thư viện của Hugging Face biến cả một câu thành một vector chất lượng cao chỉ với vài dòng code. Nhờ đó các bài classification / similarity làm được *siêu nhanh, siêu đơn giản*.

## Vì sao quan trọng

Tự train một model embedding câu tốn rất nhiều công. `sentence-transformers` gói sẵn model pretrained (vd `all-MiniLM`, `paraphrase-mpnet`) để `encode` câu → vector dùng ngay. Với nhiều bài toán, chỉ cần embedding tốt + một bước nhẹ là xong — không cần train mạng lớn.

## Dùng nhanh

```python
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer("all-MiniLM-L6-v2")

emb = model.encode(["Xin chào", "Hello there"])
sim = util.cos_sim(emb[0], emb[1])   # độ giống nhau về nghĩa
```

## Ý chính

- **Câu → vector 1 bước:** `encode()` trả embedding đã tối ưu cho *so sánh nghĩa ở mức câu* (khác embedding từng token).
- **Classification siêu nhanh:** encode câu rồi gắn một classifier nhẹ (logistic / k-NN) lên trên — không cần fine-tune cả Transformer.
- **Similarity & search:** `cos_sim` để tìm câu gần nghĩa; là lõi của [semantic-search.md](./semantic-search.md) và retrieve trong [rag.md](./rag.md).
- **Nạp vào vector DB:** vector từ `encode()` đẩy thẳng vào [vector-database.md](./vector-database.md) để tìm top-k.
- **Chọn model theo nhu cầu:** MiniLM nhẹ & nhanh; mpnet chính xác hơn nhưng nặng hơn.

## Hình minh họa

![Cosine similarity giữa hai vector câu](assets/protonx/cosine-similarity.jpg)

![Embedding: hàm biến văn bản thành vector](assets/protonx/embeddings-function.jpg)

## Trong pipeline

```
câu → SentenceTransformer.encode → vector → { cos_sim: similarity | classifier nhẹ: nhãn | vector DB: search }
```

Đây là con đường ngắn nhất từ [embedding.md](./embedding.md) tới [classification.md](./classification.md) và [semantic-search.md](./semantic-search.md) mà không phải train nặng.

## Tham khảo

- [SBERT / sentence-transformers](https://www.sbert.net/)
- Reimers & Gurevych 2019 — [Sentence-BERT](https://arxiv.org/abs/1908.10084)

## Related

- [embedding.md](./embedding.md), [classification.md](./classification.md)
- [semantic-search.md](./semantic-search.md), [vector-database.md](./vector-database.md), [huggingface.md](./huggingface.md)
