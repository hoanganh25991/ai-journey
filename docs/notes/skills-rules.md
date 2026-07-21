# Skills · Rules · Commands

> Three ways to teach a coding agent. **Skill** = packaged capability loaded when needed; **Rule** = constraint that always applies; **Command** = shortcut to kick off a workflow.

## Why it matters

The same model, loaded with the right know-how, works far better: it knows your process, follows project conventions, and you do not repeat instructions every turn. These three layers are how that "brain gets configured." Put mandatory things in rules, complex processes in skills.

## Key ideas

- **Three concepts:**

  | Kind | What | When loaded | Example |
  |------|------|-------------|---------|
  | **Skill** | folder with `SKILL.md` (+ scripts/assets) | model reads when task matches description | `graphify`, `frontend-slides`, `tavily-*` |
  | **Rule** | instructions always on or matched by glob | every turn (always) or on file pattern | commit style, "docs = notes-first" |
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

  The **description** is the most important field: write a clear trigger ("use when…") so the agent picks correctly. Skills can include scripts the agent runs via shell/MCP.

- **Global home: `~/.agents`**
  - Canonical path: `~/.agents/skills/<name>/SKILL.md`.
  - Cursor / Claude / Pi load from here → write once, use across clients.
  - Do not copy skills into `~/.cursor/skills` or `~/.claude/skills` (keep empty); Pi uses **symlinks** to `~/.agents` only.
  - Install GitHub skill packs: `~/.agents/scripts/sync-skill-repos.sh` (alias `skill-lock.sh`) — rsync copy with lockfile at `config/skill-repos.lock.json`. Do not use `npx skills` for `~/.agents`.

- **Project-local exception:** repo-specific skills may live in that repo's `.cursor/skills`. Global skills stay in `~/.agents/skills`.

- **Rules in practice:** "always" rules consume context every turn → keep them short. Glob rules (`*.tsx`, `notes/*.md`) load only on matching files → cheaper. Rules for conventions; skills for complex processes.

- **Skill interactions:** when adding a skill, consider overlap with existing ones (conflicting triggers or instructions). Anthropic Opus/Sonnet is strong at asking back to clarify interactions.

## References

- [Anthropic — Agent Skills](https://www.anthropic.com/news/skills)
- [AGENTS.md](https://agents.md/) — standard for declaring agent instructions

## Related

- [mcp.md](./mcp.md), [07-agents.md](./07-agents.md), [08-model-notes.md](./08-model-notes.md)
