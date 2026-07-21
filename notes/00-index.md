# AI Lab — Notes Index

> **Gốc = notes.** Mỗi chủ đề là một file `.md` viết như bài giải thích ngắn. Build ra hub tĩnh trong `docs/` rồi mở/serve từ đó.

Build: `./scripts/build.sh` → mở [`../docs/index.html`](../docs/index.html). Review giống GitHub Pages: `./scripts/review.sh`.

Catalog: [`catalog.json`](./catalog.json) — source of truth cho listing (id, title, summary, slides, demo).

## Ba lớp nội dung

| Lớp | Vai trò | Khi nào đọc |
|-----|---------|-------------|
| **Note** (`.md`) | Nơi **đơn giản nhất** để nắm ý chính | luôn bắt đầu ở đây |
| **Slide** (`slides/<topic>/`) | Trình bày, làm rõ bằng hình + từng bước | khi muốn giảng lại / thuyết trình |
| **Demo** (`demos/<topic>/app/`) | Thử tay ngay trong browser | khi muốn *cảm* cách nó chạy |

Một note là trung tâm; nó *có thể* trỏ tới một slide và một demo (khai trong `catalog.json`, để `null` nếu chưa có).

## Quy ước viết note

Mỗi note theo cùng một khung để dễ đọc và dễ mở rộng:

1. Tiêu đề + một câu lead (ví dụ đời thường).
2. **Vì sao quan trọng** — một đoạn ngắn.
3. **Ý chính** — 3–5 mục, kèm ví dụ nhỏ.
4. **Hình minh họa** — 1–3 ảnh, mỗi ảnh một caption.
5. **Trong pipeline** — nối sang note khác.
6. **Slides & demo** — bảng link.
7. **Tham khảo** — 1–3 link công khai (tuỳ chọn).

## Đưa hình / PDF vào note

Ảnh là cách nhanh nhất để làm rõ một ý. Cách đưa lên:

```
ảnh chụp / 1 trang PDF  →  notes/assets/<chủ-đề>/ten-file.jpg
                        →  trong note: ![caption ngắn](assets/<chủ-đề>/ten-file.jpg)
                        →  ./scripts/build.sh  →  docs/notes/*.html
```

- Copy ảnh vào `notes/assets/…` rồi tham chiếu bằng đường dẫn **tương đối** `assets/…` — build copy nguyên sang `docs/notes/assets/` nên link chạy đúng ở cả local lẫn GitHub Pages.
- Ảnh đứng riêng một dòng → tự thành `<figure>` có caption (lấy từ chữ trong `![…]`).
- **PDF phức tạp:** đừng nhúng cả file. Chụp 1–2 trang then chốt thành ảnh, hoặc để link ngoài; phần cốt lõi thì viết lại bằng lời trong note.

## Notes

| Note | Group | Slides | Demo |
|------|-------|--------|------|
| [tokenize.md](./tokenize.md) | concept | có | có |
| [embedding.md](./embedding.md) | concept | có | có |
| [attention.md](./attention.md) | concept | có | có |
| [softmax.md](./softmax.md) | concept | có | có |
| [rag.md](./rag.md) | concept | có | có |
| [mcp.md](./mcp.md) | concept | có | có |
| [skills-rules.md](./skills-rules.md) | concept | — | mcp app |
| [train-gpu.md](./train-gpu.md) | concept | — | — |
| [04-demo-car.md](./04-demo-car.md) | project | có | có |
| [05-demo-text.md](./05-demo-text.md) | project | có | có (+ complexity-router) |
| [06-train-infer.md](./06-train-infer.md) | concept | — | — |
| [07-agents.md](./07-agents.md) | concept | — | mcp app |
| [08-model-notes.md](./08-model-notes.md) | field-notes | — | — |
| [09-agent-automation.md](./09-agent-automation.md) | field-notes | Hermess | — |
| [10-ai-timeline.md](./10-ai-timeline.md) | field-notes | — | — |
| [personal-knowledge-base.md](./personal-knowledge-base.md) | project | overview | CLI / plan |

## Assets

[`assets/`](./assets/) — hình minh họa dùng trong note & slide. Thêm ảnh mới vào đây theo chủ đề rồi build lại.
