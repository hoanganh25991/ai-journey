# MCP — Model Context Protocol

> A common standard for agents to *call external tools* — like USB-C for AI. Instead of every app inventing its own plugin, every tool speaks the same protocol so any agent can plug in and use it.

## Why it matters

A model only generates text. To *do* real things — open a browser, query a database, render in Blender, search the web — it must connect to external tools. Before MCP, each integration was bespoke and non-reusable. MCP standardizes how tools are described and invoked, so one server written once runs in Cursor, Claude, Pi, and more. That is the hinge from "answering" to "executing" (see [10-ai-timeline.md](./10-ai-timeline.md)).

## Key ideas

- **Architecture:**

  ```
  Host (agent)  →  MCP client  →  MCP server  →  tool / API / process
     ↑ context                        ↓ result (JSON with schema)
     └──────────── tool call / tool result ─────────────┘
  ```

  - *Host:* where the model runs (Cursor, Claude Code, Pi…).
  - *Server:* process that exposes a tool list plus input schema (JSON Schema).
  - *Tool:* one action — navigate a browser, query a DB, render Blender, search the web.
  - Transport via stdio or HTTP; each tool declares its parameters → the model calls correctly.

- **Discover then invoke:** the model *lists* available tools, then *calls* them — no hardcoding. New tools do not require editing the model.
- **Results with schema:** JSON in a known shape → easy to parse and chain tools.
- **One standard, many clients:** the same MCP server works on every MCP-capable host.
- **Safety boundary:** tools declare parameters and permissions → the host controls what the model may do.

**MCP ≠ Skills**

| | MCP | Skills |
|--|-----|--------|
| What | executable *tools* | markdown *instructions* for doing a job well |
| Format | server + schema | `SKILL.md` + scripts |
| When | need to run an external action | need know-how / repeatable process |

See also: [skills-rules.md](./skills-rules.md).

Example MCP servers in use: **browser** (Playwright / Chrome DevTools), **blender** (`bpy`, scene inspect, render), **tavily** (web search / extract / crawl).

## References

- [Model Context Protocol — spec & docs](https://modelcontextprotocol.io/)
- [Introducing MCP (Anthropic)](https://www.anthropic.com/news/model-context-protocol)

## Related

- [07-agents.md](./07-agents.md), [skills-rules.md](./skills-rules.md), [rag.md](./rag.md)
