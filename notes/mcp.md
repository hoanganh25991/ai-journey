# MCP — Model Context Protocol

> Một chuẩn chung để agent *gọi công cụ ngoài*. Ví như cổng USB-C cho AI: thay vì mỗi app một kiểu cắm riêng, mọi tool nói cùng một "giọng" nên agent cắm vào là dùng được.

## Vì sao quan trọng

Bản thân mô hình chỉ sinh chữ; muốn nó *làm* việc thật — mở trình duyệt, truy vấn DB, render Blender, search web — phải nối ra công cụ bên ngoài. Trước MCP, mỗi tích hợp là code riêng, không tái dùng. MCP chuẩn hóa cách mô tả và gọi tool, nên một server viết một lần dùng được ở Cursor, Claude, Pi… Đây chính là bản lề đưa AI từ "trả lời" sang "thực thi" (xem [10-ai-timeline.md](./10-ai-timeline.md)).

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

- **Discover rồi invoke:** model *hỏi* server có tool gì (list) rồi mới *gọi* (call) — không hardcode. Thêm tool mới không phải sửa model.
- **Kết quả có schema:** trả JSON theo khuôn → dễ parse, dễ nối nhiều tool thành chuỗi.
- **Một chuẩn, nhiều client:** cùng một MCP server chạy được trên mọi host hỗ trợ MCP.
- **Ranh giới an toàn:** tool khai báo rõ tham số và quyền → host kiểm soát được model được phép làm gì.

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

## Tham khảo

- [Model Context Protocol — spec & docs](https://modelcontextprotocol.io/)
- [Giới thiệu MCP (Anthropic)](https://www.anthropic.com/news/model-context-protocol)

## Related

- [07-agents.md](./07-agents.md), [skills-rules.md](./skills-rules.md), [rag.md](./rag.md)
