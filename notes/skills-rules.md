# Skills · Rules · Commands

> Ba lớp "know-how" nạp vào AI coding agent. Skills = năng lực đóng gói; Rules = ràng buộc luôn áp; Commands = shortcut kích hoạt.

## Ba khái niệm

| Lớp | Là gì | Khi nào load | Ví dụ |
|-----|-------|--------------|-------|
| **Skill** | 1 folder `SKILL.md` (+ script/asset) mô tả một năng lực | model tự đọc khi task khớp description | `graphify`, `frontend-slides`, `tavily-*` |
| **Rule** | chỉ dẫn luôn áp hoặc theo pattern file | mỗi turn (always) hoặc khi match glob | commit style, "docs = notes-first" |
| **Command** | prompt / workflow gọi bằng shortcut | khi user gõ (vd `/deep-plan`) | `/graphify .`, `/loop` |

## SKILL.md — cấu trúc

```
~/.agents/skills/<name>/SKILL.md
---
name: <name>
description: khi nào dùng skill này  ← model dựa vào đây để tự kích hoạt
---
# hướng dẫn từng bước + script path
```

- **description** là phần quan trọng nhất: viết rõ trigger ("use when…") để agent tự chọn.
- Skill có thể kèm script → agent chạy qua shell/MCP.

## Global home: `~/.agents`

- Canonical: `~/.agents/skills/<name>/SKILL.md`.
- Cursor / Claude / Pi đều load từ đây → viết một lần, dùng nhiều client.
- Không copy skill vào `~/.cursor/skills` hay `~/.claude/skills` (để trống); Pi chỉ dùng **symlink** trỏ về `~/.agents`.
- Cài / khoá version: `npx skills add … -g` (lockfile ở `~/.agents/.skill-lock.json`).

## Project-local exception

Skill riêng cho một repo có thể để trong `.cursor/skills` của repo đó. Skill cá nhân/global thì vẫn ở `~/.agents/skills`.

## Rules — ghi nhớ thực chiến

- Rule "always" tốn context mỗi turn → giữ ngắn, chỉ đưa thứ thật sự bắt buộc.
- Rule theo glob (`*.tsx`, `notes/*.md`) chỉ nạp khi đụng file khớp → rẻ hơn.
- Dùng rule cho quy ước bền vững (commit, layout docs), skill cho quy trình phức tạp.

## Liên quan hệ thống

Khi thêm skill mới, cân nhắc nó **ảnh hưởng skill đang có** thế nào (chồng trigger, mâu thuẫn hướng dẫn). Anthropic Opus/Sonnet mạnh ở việc *hỏi ngược* để làm rõ tương tác này.

## Homes

- `~/.agents/skills` — skill global (source of truth)
- `~/work-station/agents-setup` — sân thử nghiệm skill / lính (weblog TODO)
- `graphify` — visualize link giữa method trong source

## Related

- [mcp.md](./mcp.md), [07-agents.md](./07-agents.md), [08-model-notes.md](./08-model-notes.md)
