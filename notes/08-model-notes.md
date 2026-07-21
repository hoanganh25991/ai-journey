# Model field notes

> **Model ≠ harness.** Đây là cảm nhận về *bản thân mô hình* (qua OpenRouter + Cursor). So sánh harness ở [07-agents.md](./07-agents.md).

## Bảng nhanh (kinh nghiệm cá nhân)

| Model / Mode | Mạnh | Yếu / chi phí |
|--------------|------|---------------|
| **Grok 4.5** | Nhanh, mượt, cảm giác rất tốt; chất lượng cao; đốt ít tiền | Không dẫn đầu mọi benchmark; hallucination cao hơn ở task không verify được |
| **Composer 2.5 Fast** | Rất nhanh, trả lời tốt | Tốn tiền hơn Auto |
| **Cursor Auto** | Feedback loop nhanh | Chất lượng dao động theo routing |
| **Anthropic Opus / Sonnet / Fable** | Hỏi ngược làm rõ context & skill cực tốt; tương tác chắc | Chậm; có session limit |
| **DeepSeek V4** | Debug / fix lỗi tốt | Không nhận ảnh; yếu khi code mới (greenfield) |
| **Qwen 3** | Task đơn giản | Yếu ở complex follow / mô tả dự án lớn không có codebase |
| **Kimi / GLM** | Code tốt | Đắt |

## Grok 4.5 — vì sao ấn tượng

Trải nghiệm: **nhanh, mượt, thật sự rất tốt** — đặc biệt khi để làm default trong Cursor thì tiền không bị đốt nhiều mà chất lượng còn *tốt hơn Auto*.

Context công khai (xAI, 2026-07) khớp cảm nhận:

- Tối ưu cho coding + agentic, phục vụ ở tốc độ ~**80 TPS** (fast-model).
- **Token efficiency**: dùng ~4.2× ít output token hơn Opus 4.8 trên SWE-Bench Pro → *rẻ hơn nhiều mỗi task* (giá $2 in / $6 out /1M).
- Benchmark ngang tầm Opus 4.8 / GPT-5.5 ở nhiều eval coding (mạnh Terminal-Bench 2.1), không dẫn đầu tuyệt đối; được train cùng Cursor.
- Điểm mạnh chính = **intelligence trên mỗi đơn vị thời gian & chi phí**, hợp task verify được bằng máy.

→ Đây chính là lý do "chạy tốt hơn Auto mà đốt ít tiền": tốc độ cao + ít token.

## Nguyên tắc rút ra

- **Greenfield** (dự án mới, ít codebase): ưu tiên model mạnh reasoning (Anthropic, Grok) hơn DeepSeek/Qwen.
- **Debug / fix trên codebase có sẵn**: DeepSeek V4 rất hiệu quả, rẻ.
- **Cần ảnh (screenshot, diagram)**: tránh DeepSeek (không nhận ảnh).
- **Cần tốc độ + chi phí thấp**: Grok 4.5 / Composer Fast.
- **Cần làm rõ ràng buộc, thiết kế skill**: Anthropic mạnh nhất ở hỏi ngược.

Related: [07-agents.md](./07-agents.md), [mcp.md](./mcp.md), [skills-rules.md](./skills-rules.md), [personal-kb.md](./personal-kb.md)
