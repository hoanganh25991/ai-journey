# LangGraph — Agents As Graphs

> LangGraph models an agent as a **state machine**: nodes do work (LLM, tools, routers), edges decide the next node. Multi-agent flows, support bots, and self-reflective RAG become drawable graphs instead of spaghetti chains. Everyday metaphor: a flowchart that can loop until a success condition.

## Why it matters

Linear “prompt → answer” chains break on routing, retries, and collaboration. Graphs make [agentic-patterns.md](./agentic-patterns.md) executable: reflection is an edge back to draft; tool use is a node; multi-agent is parallel or sequential subgraphs.

## Key ideas

- **State + nodes + edges:** shared state travels the graph; reducers merge updates.
- **Routing agents:** a classifier/router node sends traffic to the right specialist path.
- **Structured output / tool calls:** nodes emit typed objects or function calls (search, format) before continuing.
- **Multi-agent collaborate:** several agent nodes fulfill complex questions; hand off via state.
- **Self-reflective RAG:** retrieve → grade docs → rewrite query / re-retrieve → generate.
- **Web agents:** observe page → decide action (WebVoyager-style) in a loop.
- **Simple → complex bots:** start with linear support flow; add branches for auth, search, escalation.

## Pipeline

```
input → router → {tool | rag | specialist}* → (reflect?) → response
         ↑________________ loops / retries _______________|
```

## Slides & demo

| | Link |
|--|------|
| Slides | [slides/langgraph](../slides/langgraph/index.html) |
| App | [demos/langgraph/app](../demos/langgraph/app/index.html) |

## References

- LangGraph documentation — stateful multi-actor applications with LLMs

## Related

- [agentic-patterns.md](./agentic-patterns.md), [advanced-rag.md](./advanced-rag.md)
- [langsmith.md](./langsmith.md) — observe graph runs
- [mcp.md](./mcp.md) — tools the graph can call
