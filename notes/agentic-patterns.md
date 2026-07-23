# Agentic Patterns — Reflect, Tool, Plan, Multi-Agent

> Patterns are *recipes* for how an agent thinks — reflection, tool use, planning, multi-agent — independent of which IDE or model you plugged in. Everyday metaphor: study habits (outline → draft → critique) vs which notebook brand you buy.

## Why it matters

[`07-agents.md`](./07-agents.md) compares **harnesses** (Cursor, Claude Code…). This note compares **reasoning patterns** (Andrew Ng’s agentic design set and friends). Same pattern ports across harnesses; knowing both prevents “buy a new tool” when you needed a better loop.

## Key ideas

- **Reflection:** draft → critique → revise before acting (or after a tool result).
- **Tool use:** model chooses functions (search, code, browser); schemas matter as much as clever prompts.
- **Planning:** break a goal into steps; replan when observations contradict the plan.
- **Multi-agent:** specialists collaborate (researcher / writer / reviewer) with shared state — only helps if handoffs are clean.
- **Self-discover:** let the model compose its own reasoning structure for a class of tasks (meta-pattern).

## Pipeline

```
goal → (plan?) → act / tool → observe → (reflect?) → next step → done
              ↘ multi-agent: route to specialist crew
```

## Slides & demo

| | Link |
|--|------|
| Slides | [slides/agentic-patterns](../slides/agentic-patterns/index.html) |
| App | [demos/agentic-patterns/app](../demos/agentic-patterns/app/index.html) |

## References

- Andrew Ng — agentic reasoning design patterns (reflection, tools, planning, multi-agent)
- Self-Discover (arXiv 2402.03620) — LLM-composed reasoning structures

## Related

- [07-agents.md](./07-agents.md), [mcp.md](./mcp.md), [skills-rules.md](./skills-rules.md)
- [langgraph.md](./langgraph.md) — implement patterns as graphs
- [langsmith.md](./langsmith.md) — trace and evaluate those loops
