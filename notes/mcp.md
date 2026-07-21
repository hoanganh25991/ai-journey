# MCP — Model Context Protocol

> Host (Cursor / Claude / Pi) ↔ MCP server ↔ tools có schema. Cách chuẩn để agent *thực thi* ra ngoài mô hình.

## Slides & demo

| | Link |
|--|------|
| Slides | [demos/mcp/slides](../demos/mcp/slides/index.html) |
| Working app | [demos/mcp/app](../demos/mcp/app/index.html) |

## Kiến trúc

```
Host (agent)  →  MCP client  →  MCP server  →  tool / API / process
   ↑ context                        ↓ result (JSON có schema)
   └──────────── tool call / tool result ─────────────┘
```

- **Host**: nơi model chạy (Cursor, Claude Code, Pi…).
- **Server**: process expose danh sách tool + input schema (JSON Schema).
- **Tool**: một hành động cụ thể — navigate browser, query DB, render Blender, search web.
- Giao tiếp qua stdio hoặc HTTP; mỗi tool tự mô tả tham số → model gọi đúng.

## Ý chính

- Chuẩn hoá "gọi tool": thay vì mỗi app một cách tích hợp, MCP là một protocol chung.
- Model **discover** tool (list) rồi **invoke** (call) — không hardcode.
- Kết quả trả JSON có schema → dễ parse, dễ chain nhiều tool.

## MCP ≠ Skills

| | MCP | Skills |
|--|-----|--------|
| Là gì | tool có thể *thực thi* | hướng dẫn (markdown) để model làm đúng |
| Dạng | server + schema | `SKILL.md` + script |
| Khi nào | cần chạy action ra ngoài | cần know-how / quy trình lặp lại |

Xem thêm: [skills-rules.md](./skills-rules.md).

## Ví dụ MCP server đang dùng

- **browser** (Playwright / Chrome DevTools) — navigate, click, screenshot, đọc console.
- **blender** — chạy `bpy`, inspect scene, render.
- **tavily** — web search / extract / crawl khi kiến thức local không đủ.

## Homes

- `~/.agents/skills` — global skills (Cursor/Claude/Pi tự load)
- `~/work-station/agents-setup` — nơi thử nghiệm nhiều skill / lính
- Cursor Settings → MCP — khai báo server

## Related

- [07-agents.md](./07-agents.md), [skills-rules.md](./skills-rules.md), [rag.md](./rag.md)
