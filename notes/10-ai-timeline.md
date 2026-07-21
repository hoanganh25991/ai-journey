# AI timeline — my journey (2023 → present)

> Starting point: **2023** — first time learning about LLMs, then background concepts (tokenize, embedding, attention, softmax, RAG). This timeline anchors lab notes to real AI milestones and shows why focus now shifts to **agents / automation**.

> Academic roots (Transformer 2017, BERT 2018, GPT-3 2020) underpin the concepts — see [attention.md](./attention.md), [embedding.md](./embedding.md). *My journey* starts in 2023.

## Why it matters

Concepts and tools arrive in a order that made sense for me. Mapping that order against industry milestones explains why the lab went from fundamentals → RAG → agents — and which older notes still matter.

## Key ideas

- **Stage 1 — 2023: first LLM exposure and foundations**
  - Late 2022 **ChatGPT (GPT-3.5)** made AI mainstream → 2023 I started learning seriously.
  - **March 2023** — GPT-4 · Claude 1 · Llama 1; RAG exploded.
  - Learned in order: [tokenize.md](./tokenize.md) → [embedding.md](./embedding.md) → [attention.md](./attention.md) → [softmax.md](./softmax.md).
  - Then retrieval: [rag.md](./rag.md); train → infer: [06-train-infer.md](./06-train-infer.md), [train-gpu.md](./train-gpu.md).
  - **July 2023** — Claude 2 · Llama 2. **December 2023** — Gemini 1.0 · Mixtral (MoE open).

- **Stage 2 — 2024: stronger models + early coding agents**
  - Gemini 1.5 (1M context) · Claude 3 → 3.5 Sonnet (coding jump — Cursor took off) · GPT-4o · Llama 3.1 405B · o1 · DeepSeek V3.
  - Shift from *reading concepts* to *using AI to code for real*.

- **Stage 3 — late 2024–2025: agent era (MCP · skills · harness)**
  - Lab pivots to **MCP · skills · harness**.
  - **November 25, 2024** — **MCP** (Anthropic): standard agent ↔ tool connection. Hinge. See [mcp.md](./mcp.md).
  - **January 2025** — DeepSeek R1 — [08-model-notes.md](./08-model-notes.md).
  - **February 2025** — Claude 3.7 Sonnet · GPT-4.5. **March 2025** — MCP Streamable HTTP + OAuth · Gemini 2.5 Pro.
  - **May 2025** — Claude 4 → **Claude Code** as strong harness: [07-agents.md](./07-agents.md).
  - **August 2025** — GPT-5. **November 2025** — Claude Opus 4.5 · **AGENTS.md** standard · skills/rules: [skills-rules.md](./skills-rules.md).

- **Stage 4 — 2026: model wave + automation (now)**
  - Focus: [08-model-notes.md](./08-model-notes.md), [09-agent-automation.md](./09-agent-automation.md).
  - **April 2026** — GPT-5.5. **May 28, 2026** — Claude Opus 4.8. **June 2026** — Claude Fable 5 · Sonnet 5.
  - **July 8, 2026** — **Grok 4.5** (trained with Cursor): fast, token-efficient, cheap. **July 9, 2026** — GPT-5.6.
  - Parallel: **OpenClaw** (`pi` harness) opens "agent controls everything" → **Hermess** polishes it.

- **Milestone table:**

  | When | Event | In the lab |
  |------|-------|------------|
  | **2023** | first LLM exposure (ChatGPT/GPT-4) | start studying |
  | March 2023 | GPT-4, Claude 1, Llama 1 | tokenize · embedding · attention · softmax · RAG |
  | 2024 | Gemini 1.5, Claude 3.5, GPT-4o, o1 | coding agents |
  | **Nov 2024** | **MCP launches** | mcp |
  | 2025 | Claude 4 / GPT-5 / R1 · AGENTS.md | harness, skills |
  | 2026 | Grok 4.5, Opus 4.8, GPT-5.6 | model notes, automation |

- **Takeaways:** journey goes from **understanding models** (2023–2024) → **steering agents** (late 2024 onward). MCP (November 2024) is the hinge. 2023 concepts are not outdated — tokenize / attention / RAG still underpin every agent. Watch harnesses (Cursor / Claude Code / pi), model waves (Grok 4.5…), automation (OpenClaw / Hermess).

## Related

- [07-agents.md](./07-agents.md), [08-model-notes.md](./08-model-notes.md), [09-agent-automation.md](./09-agent-automation.md), [mcp.md](./mcp.md)
