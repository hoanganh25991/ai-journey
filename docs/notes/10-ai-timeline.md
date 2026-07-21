# AI timeline — hành trình của tôi (2023 → nay)

> Mốc bắt đầu là **2023** — lần đầu tôi biết đến LLM, rồi mới đi tìm hiểu các khái niệm nền (tokenize, embedding, attention, softmax, RAG). Timeline này neo các note của lab vào dòng thời gian AI thực tế, và cho thấy vì sao giờ trọng tâm chuyển sang **agent / automation**.

> Nền học thuật có từ trước (Transformer 2017, BERT 2018, GPT-3 2020) — là gốc của các khái niệm, xem [attention.md](./attention.md), [embedding.md](./embedding.md). Nhưng *hành trình của tôi* bắt đầu từ 2023.

## 4 giai đoạn

### 1. 2023 — Lần đầu biết LLM & học nền tảng
Cú hích: cuối 2022 **ChatGPT (GPT-3.5)** làm AI thành sản phẩm đại chúng → 2023 tôi bắt đầu tìm hiểu nghiêm túc. Đây là phần **concepts** của lab.
- **03/2023** — GPT-4 · Claude 1 · Llama 1 (open weights). RAG bùng nổ.
- Đi học khái niệm nền theo thứ tự: [tokenize.md](./tokenize.md) → [embedding.md](./embedding.md) → [attention.md](./attention.md) → [softmax.md](./softmax.md).
- Rồi tới retrieval: [rag.md](./rag.md); train → infer: [06-train-infer.md](./06-train-infer.md), [train-gpu.md](./train-gpu.md).
- **07/2023** — Claude 2 · Llama 2 (open, dùng thương mại). **12/2023** — Gemini 1.0 · Mixtral (MoE open).

### 2. 2024 — Model mạnh hơn + chớm agent code
- **Gemini 1.5** (1M context) · **Claude 3 → 3.5 Sonnet** (bước nhảy về code — thời Cursor cất cánh) · **GPT-4o** (đa phương thức) · **Llama 3.1 405B** · **o1** (reasoning) · **DeepSeek V3**.
- Tôi chuyển từ *đọc khái niệm* sang *dùng AI để code thật*.

### 3. Cuối 2024 – 2025 — Kỷ nguyên agent (MCP · skills · harness)
Lúc lab chuyển sang **MCP · skills · harness**.
- **25/11/2024** — **MCP** (Anthropic): chuẩn kết nối agent ↔ tool. Bản lề. Xem [mcp.md](./mcp.md).
- **01/2025** — DeepSeek R1 (reasoning open, rẻ) — [08-model-notes.md](./08-model-notes.md).
- **02/2025** — Claude 3.7 Sonnet · GPT-4.5. **03/2025** — MCP thêm Streamable HTTP + OAuth · Gemini 2.5 Pro.
- **05/2025** — Claude 4 (Sonnet/Opus) → **Claude Code** thành harness mạnh: [07-agents.md](./07-agents.md).
- **08/2025** — GPT-5. **11/2025** — Claude Opus 4.5 · **AGENTS.md** thành chuẩn · skills/rules: [skills-rules.md](./skills-rules.md).

### 4. 2026 — Model wave + automation (bây giờ)
Trọng tâm hiện tại: [08-model-notes.md](./08-model-notes.md), [09-agent-automation.md](./09-agent-automation.md).
- **04/2026** — GPT-5.5. **28/05/2026** — Claude Opus 4.8. **06/2026** — Claude Fable 5 · Sonnet 5.
- **08/07/2026** — **Grok 4.5** (train cùng Cursor): nhanh, token-efficient, rẻ. **09/07/2026** — GPT-5.6.
- Song song: **OpenClaw** (harness `pi`) mở màn cảm giác agent control mọi thứ → **Hermess** làm tốt.

## Bảng mốc chính

| Thời điểm | Sự kiện | Trong lab |
|-----------|---------|-----------|
| **2023** | **Lần đầu biết LLM** (ChatGPT/GPT-4) | bắt đầu học |
| 03/2023 | GPT-4, Claude 1, Llama 1 | tokenize · embedding · attention · softmax · RAG |
| 2024 | Gemini 1.5, Claude 3.5, GPT-4o, o1 | code agents |
| **11/2024** | **MCP ra đời** | mcp |
| 2025 | Claude 4 / GPT-5 / R1 · AGENTS.md | harness, skills |
| 2026 | Grok 4.5, Opus 4.8, GPT-5.6 | model notes, automation |

## Ý rút ra

- Hành trình đi từ **hiểu mô hình** (2023–2024) → **điều khiển agent** (cuối 2024 →). MCP (11/2024) là bản lề.
- Concepts học năm 2023 *không lỗi thời*: tokenize / attention / RAG vẫn là nền cho mọi agent hôm nay.
- Cái mới cần theo: harness (Cursor / Claude Code / pi), model wave (Grok 4.5…), automation (OpenClaw / Hermess).

## Related

- [07-agents.md](./07-agents.md), [08-model-notes.md](./08-model-notes.md), [09-agent-automation.md](./09-agent-automation.md), [mcp.md](./mcp.md)
