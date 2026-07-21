# Skills · Rules · Commands

> Three ways to teach a coding agent. **Skill** = packaged capability loaded when needed; **Rule** = constraint that always applies; **Command** = shortcut to kick off a workflow. Everyday metaphor: skills are toolboxes you open for a job, rules are house laws on the wall, commands are buttons you press.

## Why it matters

The same model, loaded with the right know-how, works far better: it knows your process, follows project conventions, and you do not repeat instructions every turn. These three layers are how that “brain gets configured.” Put mandatory things in rules, complex processes in skills, and frequent workflows in commands.

Without this split, agents either ignore your conventions or burn context repeating them.

## Key ideas

- **Three concepts:**

  | Kind | What | When loaded | Example |
  |------|------|-------------|---------|
  | **Skill** | folder with `SKILL.md` (+ scripts/assets) | model reads when task matches description | `graphify`, `frontend-slides`, `tavily-*` |
  | **Rule** | instructions always on or matched by glob | every turn (always) or on file pattern | commit style, “docs = notes-first” |
  | **Command** | prompt / workflow via shortcut | user types it (e.g. `/deep-plan`) | `/graphify .`, `/loop` |

- **SKILL.md structure:**

  ```
  ~/.agents/skills/<name>/SKILL.md
  ---
  name: <name>
  description: when to use this skill  ← model uses this to auto-trigger
  ---
  # step-by-step guide + script paths
  ```

  The **description** is the most important field: write a clear trigger (“use when…”) so the agent picks correctly. Skills can include scripts the agent runs via shell/MCP.

- **Global home: `~/.agents`**
  - Canonical path: `~/.agents/skills/<name>/SKILL.md`.
  - Cursor / Claude / Pi load from here → write once, use across clients.
  - Do not copy skills into `~/.cursor/skills` or `~/.claude/skills` (keep empty); Pi uses **symlinks** to `~/.agents` only.
  - Install GitHub skill packs with the custom manager (`skill.sh` / lockfile) — not `npx skills` for `~/.agents`.

- **Project-local exception:** repo-specific skills may live in that repo’s `.cursor/skills`. Global skills stay in `~/.agents/skills`.

- **Rules in practice:** “always” rules consume context every turn → keep them short. Glob rules (`*.tsx`, `notes/*.md`) load only on matching files → cheaper. Rules for conventions; skills for complex processes.

- **Skill interactions:** when adding a skill, consider overlap with existing ones (conflicting triggers or instructions). Strong models (Opus/Sonnet) often ask back to clarify interactions — design descriptions to reduce collisions.

## Worked example (intuition)

You want every AI Lab change to stay notes-first. Put a short **rule** on `notes/**`. When you ask for a new deck, the agent loads **frontend-slides** skill because the description matches “create presentation.” You type `/graphify .` as a **command** when you need a fresh knowledge graph — no essay required.

## Common pitfalls

- **Always-rules that are novels** — waste tokens every turn; split into globs/skills.
- **Vague skill descriptions** — agent never auto-triggers, or triggers on everything.
- **Duplicating skill trees** into Cursor/Claude folders — drift and double maintenance.
- **Conflicting skills** — two skills claim the same trigger with opposite steps.

## Illustrations

![Skill vs Rule vs Command](assets/skills-rules/skills-rules-commands.png)

![Three layers side by side](assets/skills-rules/skills-layers.svg)

## Pipeline

```
task → (rules always/glob) + (matching skills) + (optional /command) → agent acts with MCP/tools
```

## Slides & demo

| | Link |
|--|------|
| Slides | [slides/skills-rules](../slides/skills-rules/index.html) |
| MCP demo | [demos/mcp](../demos/mcp/app/index.html) |

## References

- [Anthropic — Agent Skills](https://www.anthropic.com/news/skills)
- [AGENTS.md](https://agents.md/) — standard for declaring agent instructions

## Related

- [mcp.md](./mcp.md), [07-agents.md](./07-agents.md), [08-model-notes.md](./08-model-notes.md)
