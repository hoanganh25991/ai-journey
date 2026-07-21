# Roadmap · hành trình AI Lab

> Bản đồ vui để đi hết 25 note. Không cần học thẳng một mạch — chọn một **màn** hợp mood, click vào, xong thì sang màn kế.

Mốc thời gian trên card hub chỉ để đọc như một chuyến đi 2023 → 2026; thứ tự dưới đây là **thứ tự học gợi ý**.

## Bản đồ nhanh (5 màn)

```
  ① ABC máy đọc chữ          ①→④
  ② Build model & train      ⑤→⑪
  ③ Tìm kiếm & RAG           ⑫→⑭
  ④ Thử tay trong lab        ⑰→⑳
  ⑤ Agent cầm tay làm        ⑮→⑯ · ㉑→㉕
```

```
START
  │
  ▼
┌─────────────────────────────┐
│ ① ABC · máy đọc chữ         │  tokenize → embedding → attention → softmax
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│ ② Build · train · chạy      │  classification → PyTorch / TF → HF / Kaggle
│                             │  → Transformer → sentence-transformers
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│ ③ Tìm · neo vào tài liệu    │  RAG → vector DB → semantic-search
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│ ④ Demo · thấy tận mắt       │  car-nn · sentiment · train↔infer · GPU
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│ ⑤ Agent · điều khiển máy    │  MCP · skills · harness · automation · KB
└──────────────┬──────────────┘
               ▼
             YOU ARE HERE 🎉
```

---

## ① ABC — máy đọc chữ (01 → 04)

> Mục tiêu: hiểu máy biến câu thành số, rồi “nhìn” và “chọn”.

| # | Khi | Note | Một câu nhớ |
|---|-----|------|-------------|
| 01 | 01/2023 | [Tokenize](./tokenize.md) | Cắt chữ → ID. Máy không đọc chữ. |
| 02 | 03/2023 | [Embedding](./embedding.md) | Gần nghĩa → gần trong không gian số. |
| 03 | 05/2023 | [Attention](./attention.md) | Mỗi từ tự quyết định nhìn chỗ nào. |
| 04 | 06/2023 | [Softmax](./softmax.md) | Điểm thô → phần trăm, cộng = 1. |

**Boss màn này:** đọc xong còn giải thích được “chó / mèo gần nhau hơn chó / hóa đơn” bằng embedding + cosine.

---

## ② Build model & train (05 → 11)

> Mục tiêu: tự tay dán nhãn, train vài epoch, biết lấy data & model ở đâu.

| # | Khi | Note | Một câu nhớ |
|---|-----|------|-------------|
| 05 | 08/2023 | [Classification](./classification.md) | Head + softmax = dán nhãn. |
| 06 | 10/2023 | [Train với PyTorch](./pytorch-training.md) | forward → loss → backward → step. |
| 07 | 11/2023 | [Train với TensorFlow](./tensorflow-training.md) | `compile` rồi `fit` — Keras lo vòng lặp. |
| 08 | 01/2024 | [Hugging Face](./huggingface.md) | Dataset + model pretrained + Spaces. |
| 09 | 03/2024 | [Kaggle](./kaggle.md) | Dataset + notebook GPU miễn phí. |
| 10 | 05/2024 | [Transformer](./transformer.md) | Xếp chồng attention = khung LLM. |
| 11 | 07/2024 | [sentence-transformers](./sentence-transformers.md) | Câu → vector vài dòng; classify siêu nhanh. |

**Boss màn này:** train được một classifier nhỏ (PyTorch *hoặc* TF) rồi encode câu bằng sentence-transformers không cần viết lại cả mạng.

---

## ③ Tìm kiếm & RAG (12 → 14)

> Mục tiêu: đừng bắt model “nhớ hết” — cho nó tra cứu rồi mới trả lời.

| # | Khi | Note | Một câu nhớ |
|---|-----|------|-------------|
| 12 | 08/2024 | [RAG](./rag.md) | Tra trước, soạn sau + trích dẫn. |
| 13 | 10/2024 | [Vector database](./vector-database.md) | Kho vector + tìm top-k hàng xóm. |
| 14 | 12/2024 | [Semantic search](./semantic-search.md) | Hybrid / tiered / fallback — bài học RAG thật. |

**Boss màn này:** phân biệt được keyword (Elastic) vs nghĩa (embedding), và vì sao hybrid thường thắng.

Repo tham chiếu: [semantic-search](https://github.com/hoanganh25991/semantic-search).

---

## ④ Thử tay trong lab (17 → 20)

> Mục tiêu: thấy model *làm việc* trong browser — không còn chỉ đọc lý thuyết.

| # | Khi | Note | Một câu nhớ |
|---|-----|------|-------------|
| 17 | 05/2025 | [Train · GPU](./train-gpu.md) | Stack thật: PyTorch/TF + HF/Kaggle + GPU. |
| 18 | 07/2025 | [Car NN](./04-demo-car.md) | 3 cảm biến → 4 hành động. |
| 19 | 09/2025 | [Sentiment & routing](./05-demo-text.md) | Phân loại cảm xúc + định tuyến dễ/khó. |
| 20 | 10/2025 | [Train → Inference](./06-train-infer.md) | Học nặng một lần, dùng nhẹ nhiều lần. |

**Boss màn này:** mở được demo car-nn hoặc sentiment và chỉ được chỗ nào là softmax / classification head.

---

## ⑤ Agent — cầm tay làm (15 → 16 · 21 → 25)

> Mục tiêu: từ “model trả lời” sang “agent điều khiển máy”.

| # | Khi | Note | Một câu nhớ |
|---|-----|------|-------------|
| 15 | 01/2025 | [MCP](./mcp.md) | Cổng USB-C cho AI gọi tool. |
| 16 | 03/2025 | [Skills · Rules · Commands](./skills-rules.md) | Ba lớp “dạy nghề” cho agent. |
| 21 | 12/2025 | [AI Agents · harness](./07-agents.md) | Harness ≠ model — Cursor / Claude / Pi… |
| 22 | 02/2026 | [Model field notes](./08-model-notes.md) | Cảm nhận Grok / Opus / DeepSeek… |
| 23 | 03/2026 | [Agent automation](./09-agent-automation.md) | OpenClaw mở màn → Hermess làm tốt. |
| 24 | 05/2026 | [AI timeline](./10-ai-timeline.md) | Neo lab vào dòng thời gian AI thật. |
| 25 | 07/2026 | [Personal Knowledge-base](./personal-knowledge-base.md) | Search video / docs / GitHub + Graph RAG. |

**Boss màn này:** giải thích được MCP ≠ Skills, và vì sao cùng một model chạy Cursor vs Claude Code cảm giác khác hẳn.

---

## Gợi ý lộ trình (tuỳ mood)

| Mood hôm nay | Đi đường này |
|--------------|--------------|
| Mới bắt đầu, muốn nền | ① ABC (01→04) rồi dừng uống trà |
| Muốn *làm* model | ① → ② (05→11), bỏ qua agent |
| Đang làm search / chatbot | ① → ③ (12→14), xem thêm 11 |
| Thích demo vui | ④ thẳng (18, 19) rồi quay lại ① nếu bí |
| Làm việc với coding agent | ⑤ (15, 16, 21…) — đọc 22 khi chọn model |

## Một dòng chốt

```
đọc chữ → dán nhãn → tìm tài liệu → thử tay → để agent làm
   ①          ②            ③           ④            ⑤
```

Xong một màn thì quay lại hub, search theo `#topic`, hoặc mở note kế trong bảng trên.
