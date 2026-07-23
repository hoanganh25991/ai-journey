# LangSmith — Trace, Playground, Evaluate

> LangSmith is the **observability and eval** layer for LangChain/LangGraph: every run becomes a trace, prompts can be played with, and datasets score quality over time. Everyday metaphor: flight recorder + practice simulator + exam for your agents.

## Why it matters

Without traces you cannot debug a graph. Without evals you ship vibes. LangSmith (and similar tools) close the loop: change a prompt or node → see latency, tokens, failures → measure against a golden set.

## Key ideas

- **Traces:** nested spans for LLM calls, tools, retrievers — open a failed run and see which node lied.
- **Prompt playground:** edit templates with variables; compare variants before coding.
- **Evaluation:** dataset of inputs + expected traits; automatic or LLM-as-judge scorers; track regressions.
- **Pairs with graphs:** [langgraph.md](./langgraph.md) runs should be traced by default in production-like labs.

## Pipeline

```
graph / chain run → trace spans → inspect
datasets → evaluate → scores → improve prompt / graph → re-run
```

## Slides & demo

| | Link |
|--|------|
| Slides | [slides/langsmith](../slides/langsmith/index.html) |
| App | [demos/langsmith/app](../demos/langsmith/app/index.html) |

## References

- LangSmith docs — tracing, evaluation, prompt hub

## Related

- [langgraph.md](./langgraph.md), [agentic-patterns.md](./agentic-patterns.md)
- [rag.md](./rag.md), [advanced-rag.md](./advanced-rag.md) — retrieval quality shows up in evals
