# AI Agents · So sánh harness

> **Harness ≠ model.** Harness = phần mềm điều phối (UI, tool-calling, context, agent loop). Model = bộ não cắm vào. Cùng một model chạy trên harness khác nhau cho trải nghiệm rất khác. So sánh model ở [08-model-notes.md](./08-model-notes.md).

## Related demos

- [MCP](../demos/mcp/) — tools protocol
- [Complexity router](../demos/complexity-router/) — simple vs crew
- Notes: [mcp.md](./mcp.md), [skills-rules.md](./skills-rules.md), [08-model-notes.md](./08-model-notes.md)

## Bảng so sánh (kinh nghiệm cá nhân)

| Harness | Điểm mạnh | Hạn chế | Cảm nhận |
|---------|-----------|---------|----------|
| **Cursor** | Vòng feedback nhanh — thấy kết quả là chỉnh ngay; Auto vs model cố định linh hoạt; MCP + skills tốt | Auto đôi khi khó đoán chất lượng | Tương tác nhanh nhất; default `grok-4.5` đốt ít tiền mà chất lượng rất tốt |
| **Claude Code** | Clarify context cực mạnh — hỏi ngược để làm rõ; xử lý skill/rule phức tạp tốt | Chậm; có session limit → phải chờ | Chắc tay, hợp task khó / nhiều ràng buộc |
| **Pi** | Tự load `~/.agents` global; nhẹ | Hệ sinh thái nhỏ hơn | Tiện dùng chung skill với Cursor/Claude |
| **Cline / Kilo** | Open, tuỳ biến; Kilo là clone của Cline | Chất lượng phụ thuộc model cắm vào | Thử nghiệm nhanh, tự kiểm soát |
| **OpenCode** | Open-source, chạy nhiều model | Ít tính năng "smart" hơn Cursor | Tốt để test model qua OpenRouter |
| **Zed** | Editor nhanh, agent tích hợp gọn | Agent chưa sâu bằng Cursor/Claude | Nhẹ, hợp code nhanh |

## Auto vs model cố định

- **Cursor Auto**: nhanh, feedback loop tốt, nhưng chất lượng dao động theo model được route.
- **Model cố định** (vd đặt `grok-4.5`): kiểm soát được, và trải nghiệm cá nhân thấy `grok-4.5` chạy *tốt hơn* Auto mà **không đốt nhiều tiền** — cần investigate vì sao (token efficiency? routing?).

## Điều gì tạo khác biệt giữa harness

- **Context management**: cách nén / chọn file đưa vào prompt.
- **Tool calling**: MCP, shell, browser — độ mượt và độ tin cậy.
- **Agent loop**: có tự sửa lỗi, chạy test, hỏi ngược không.
- **Skills / rules**: có nạp know-how global (`~/.agents`) không.

## First mate

Orchestrate crew + `agents.md` — một agent "biết phải làm gì", điều phối các crewmate. Search Lab UI: video Kun Chen + repo `kunchenguid/firstmate`.

## Homes

- `~/.agents/skills` — global skills
- `~/work-station/agents-setup` — skill trials
- `graphify` — method link viz

## Tham khảo

- [AGENTS.md](https://agents.md/) — chuẩn khai báo hướng dẫn cho agent
- [Cursor docs](https://docs.cursor.com/) · [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
