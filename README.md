# AI Lab

**Notes là gốc.** Một pipeline build mọi thứ ra `docs/` — mở / serve chỉ từ đó. Search là trọng tâm, theme sáng.

## Build (lệnh cần chạy)

Sau khi sửa bất kỳ `notes/*.md`, `notes/catalog.json`, hay `demos/` — chạy **một lệnh**:

```bash
cd /Users/anhle/work-station/ai-lab
python3 scripts/build-docs.py
```

Nó build lại toàn bộ: hub `docs/index.html`, các trang note `docs/notes/*.html`, copy `demos/` + `slides/`, và `search-index.json`.

## Review (build + serve, giống GitHub Pages)

GitHub Pages publish repo này ở **sub-path** `https://<user>.github.io/ai-lab/`, nên `docs/` chạy ở `.../ai-lab/docs/…`. Script sau **build rồi serve dưới đúng sub-path `/ai-lab`** để link/ảnh resolve y hệt production:

```bash
python3 scripts/serve-docs.py
# → http://127.0.0.1:8080/ai-lab/docs/index.html   (tự mở browser)
```

Tùy chọn: `--port 9000`, `--no-build` (chỉ serve), `--no-open`, `--base /ai-lab`.

Mở nhanh không cần sub-path (link tương đối vẫn ổn):

```bash
open docs/index.html
```

> Mọi link trong `docs/` đều **tương đối** → chạy đúng ở cả `/ai-lab/docs/` (GitHub) lẫn mở trực tiếp. Ảnh protonx: source `notes/assets/protonx/` → build copy sang `docs/notes/assets/protonx/`.

> Hành trình 2023 → nay (lần đầu biết LLM → embedding… → agent/automation), neo vào mốc AI thực tế: [`notes/10-ai-timeline.md`](notes/10-ai-timeline.md).

## Pipeline

```
notes/*.md + notes/catalog.json     # knowledge — source of truth
demos/** + slides/** + _shared      # decks / working apps (HTML)
        │
        ▼  python3 scripts/build-docs.py
docs/                               # OUTPUT — chỗ duy nhất để mở / serve
  index.html                        # hub: search-first, list view
  notes/<id>.html                   # document view mỗi note
  demos/**  slides/**               # copy của decks / apps
  search-index.json
```

Root `index.html` chỉ redirect sang `docs/index.html`. Không sửa file trong `docs/` — nó là output.

## Search (client-side, thông minh)

- Chỉ quét **notes** (không phải video/GitHub — xem note Personal KB).
- Synonym (vd `tokenizer`≈`tokenize`≈`bpe`), rank theo title/topics/summary/body, snippet + highlight.
- `?q=…` deep-link; `?note=<id>` mở thẳng note page.
- Ít kết quả → gợi ý follow-up (topic liên quan trong catalog).

## Sửa nội dung

1. Viết / sửa `notes/*.md`
2. Khai báo trong [`notes/catalog.json`](notes/catalog.json) (`slides` / `demo` = `null` nếu chưa có)
3. `python3 scripts/build-docs.py`

## Personal KB (repo riêng)

Search videos · docs · GitHub · **Graph RAG** — ở [`~/work-station/personal-kb`](../personal-kb) (sẽ gắn submodule). Xem note [`notes/personal-kb.md`](notes/personal-kb.md).
