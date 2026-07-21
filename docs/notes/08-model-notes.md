# Model Field Notes

> **Model ≠ harness.** Notes on *the models themselves* (via OpenRouter + Cursor). Compare harnesses at [07-agents.md](./07-agents.md). Everyday metaphor: engines (models) vs cars (harnesses) — swap engines carefully; don’t blame the engine for a missing steering wheel.

## Why it matters

Harness choice shapes daily workflow; model choice shapes reasoning quality, speed, and cost. These are personal field notes — not benchmarks — on what each model feels like in real coding work.

Use them as a starting map: greenfield vs debug, image needs, and budget change the winner.

## Key ideas

- **Quick table (personal experience):**

  | Model / mode | Strong | Weak / cost |
  |--------------|--------|-------------|
  | **Grok 4.5** | fast, smooth, high quality; moderate spend | not top on every benchmark; more hallucination on unverifiable tasks |
  | **Composer 2.5 Fast** | very fast, good replies | costs more than Auto |
  | **Cursor Auto** | fast feedback loop | quality varies with routing |
  | **Anthropic Opus / Sonnet / Fable** | best at clarifying context and skills; reliable interaction | slow; session limits |
  | **DeepSeek V4** | strong debug / fix on existing code | no images; weaker on greenfield |
  | **Qwen 3** | simple tasks | weak on complex following / describing large projects without codebase |
  | **Kimi / GLM** | good code | expensive |

- **Task → model map (practical):**

  | Task shape | First pick | Runner-up | Skip |
  |------------|------------|-----------|------|
  | Greenfield scaffold / architecture | Grok 4.5 or Anthropic | Composer Fast if speed-critical | DeepSeek / Qwen alone on empty repos |
  | Debug / fix in a large existing tree | DeepSeek V4 | Grok 4.5 | Tiny “simple task” models for subtle bugs |
  | Skill / rule design, ask-back needed | Anthropic (Opus/Sonnet/Fable) | Grok | Auto when constraints must be explicit |
  | Screenshot / diagram / UI bug from image | Vision-capable (Grok / Anthropic / GPT family) | — | DeepSeek (no image input) |
  | Cheap high-volume edits | Grok 4.5 / Auto | Composer Fast | Always-Opus for typo fixes |
  | Long verifiable coding agent loops | Grok 4.5 (token-efficient) or pinned Sonnet | — | Unlogged Auto mid-refactor |

- **Grok 4.5 — why it impresses:** fast, smooth, genuinely good — especially as Cursor default; does not burn much budget yet often beats Auto. Public context (xAI, mid-2026): optimized for coding + agentic at ~**80 TPS**; ~**4.2× fewer output tokens** than Opus 4.8 on SWE-Bench Pro → much cheaper per task ($2 in / $6 out per 1M). Benchmarks competitive with Opus 4.8 / GPT-5.5 on many coding evals; trained with Cursor. Main edge = **intelligence per unit time and cost** on verifiable tasks. Watch for overconfidence when you cannot run tests.

- **Principles:**
  - *Greenfield* (new project, thin codebase): favor strong reasoning (Anthropic, Grok) over DeepSeek/Qwen.
  - *Debug / fix on existing code:* DeepSeek V4 is effective and cheap.
  - *Needs images (screenshots, diagrams):* avoid DeepSeek (no image input).
  - *Speed + low cost:* Grok 4.5 / Composer Fast.
  - *Clarifying constraints and skill design:* Anthropic strongest at asking back.
  - *Verifiable vs vibes:* prefer models that stay short and correct when tests exist; prefer ask-back models when requirements are fuzzy.

- **Re-check prices:** OpenRouter and vendor pages move — treat $ numbers as snapshots, not eternal truth. Re-read TPS/cost claims quarterly.

## Worked example (intuition)

| ID | Prompt gist | Model choice | Why |
|----|-------------|--------------|-----|
| **A** | “Scaffold a notes-first docs site with catalog + journey.” | Grok 4.5 or Anthropic | Greenfield structure; needs coherent IA, not a local stack trace |
| **B** | “This pytest fails in `train_loop.py` line 142; repo is large.” | DeepSeek V4 or Grok | Local reasoning + cheap iteration; codebase already exists |
| **C** | “Read this screenshot of the broken settings UI.” | Vision model (not DeepSeek) | Image tokens required; text-only models invent layouts |
| **D** | “Draft a skill that must coexist with graphify + frontend-slides.” | Anthropic | Ask-back on overlaps; skill-description design |
| **E** | “Rename a prop across 3 files.” | Auto or Grok | Don’t spend Opus tokens on mechanical edits |

After the run: if A looks shallow, switch harness context (pin files) before switching models. If B loops without running tests, fix tools ([07-agents.md](./07-agents.md)), not the model card.

## Common pitfalls

- **One model for every job** — waste money or quality.
- **Trusting marketing TPS without task fit** — fast wrong answers still waste time.
- **Ignoring image capability** — vision tasks silently degrade.
- **Confusing Auto routing with a single model’s skill**.
- **Upgrading model when the harness can’t run tests** — pays more for the same blindfold.

## Illustrations

![Model spectrum: fast/cheap ↔ deep/slow](assets/model-notes/model-notes-spectrum.png)

![Model vs harness reminder](assets/model-notes/model-vs-harness.png)

## Deeper dive

- **Optimize for task shape, not leaderboard rank:** SWE-bench winners can still be wrong for greenfield product sense, and vice versa. Keep a personal matrix (above) and update it when a model surprises you twice.
- **Token economics beat sticker price:** a “cheap” model that writes 4× more tokens can cost more than a “expensive” terse model. Grok’s edge on SWE-Bench Pro is partly **output brevity** under agent loops.
- **Hallucination surface:** unverifiable tasks (obscure APIs, guessed configs) punish confident models. Force tool use (read file, curl docs) or pick ask-back Anthropic when stakes are high.
- **Vision is a hard gate:** if the user attaches an image, filter the model list first. Don’t route to DeepSeek and hope.
- **Pair with harness axes:** a strong model in a tool-poor harness underperforms a mid model with shell+MCP. Diagnose harness before model ([07-agents.md](./07-agents.md)).
- **Session limits and latency:** Opus-quality sessions that hit caps mid-refactor cost more in human time than a slightly weaker unlimited loop. Plan task chunks accordingly.
- **Re-benchmark on your repo:** run the same failing test / same scaffold prompt quarterly; field notes rot when vendors ship silent updates.
- **Two-strike update rule.** Change a row in your personal matrix only after the same surprise happens twice (or once with hard evidence: tests, screenshots). One lucky/unlucky chat is noise.
- **Cost caps as product decisions.** Set a soft $/day or token budget for exploratory Auto use; pin models for long agents. Unbounded Auto + huge context is how “cheap” defaults become expensive weekends.

## Decision guide

| Situation | Prefer | Avoid / why |
|-----------|--------|-------------|
| Empty repo / new architecture | Grok or Anthropic | DeepSeek/Qwen as sole brain — weaker greenfield feel |
| Failing tests in a known codebase | DeepSeek V4 (or Grok) | Burning Opus on every red CI without trying a cheap debugger |
| Screenshot or diagram attached | Vision-capable model | DeepSeek — no image input; will guess UI |
| Designing skills/rules with conflicts | Anthropic (clarifying) | Auto that never asks and invents policy |
| High-volume small edits | Grok 4.5 / Auto / Composer Fast | Always-max model — cost without quality gain |
| Need reproducible long agent run | Pinned model + logged id | Untracked Auto routing mid-task |

## Case study

Route five real prompts without defaulting to “always Opus.”

- **Inputs:** prompts A–E from the worked table (scaffold site, failing pytest, UI screenshot, skill draft, rename prop).
- **Steps:** A → Grok/Anthropic (greenfield); B → DeepSeek/Grok (debug in-tree); C → vision model only; D → Anthropic ask-back; E → Auto/Grok cheap edit. After each run, decide whether to change **harness context** before changing model.
- **Output:** lower spend on mechanical edits; fewer blind UI guesses; skill design gets clarifying questions.
- **What you'd check:** image gate before model pick; tools available on debug tasks; token volume not just $/1M sticker; quarterly re-run of A/B prompts after vendor updates.

## Lab checklist

- [ ] Copy the task→model map into your own notes and mark what you have access to
- [ ] Run one greenfield and one debug prompt on two different models; compare outcomes
- [ ] Attach a screenshot once and verify you did **not** route to a text-only model
- [ ] Price a real task using output tokens × $/1M, not sticker rank alone
- [ ] Pin a model for a long refactor and log the model id in the PR/summary
- [ ] When quality drops, check harness tools before upgrading the model
- [ ] Revisit OpenRouter/vendor pricing and refresh any $ numbers in your notes
- [ ] Update your matrix only after a two-strike surprise (or hard evidence)

## Slides & demo

| | Link |
|--|------|
| Slides | [slides/model-notes](../slides/model-notes/index.html) |

## References

- [OpenRouter — models & prices](https://openrouter.ai/models)
- [LMArena leaderboard](https://lmarena.ai/) — ranked by human votes

## Related

- [07-agents.md](./07-agents.md), [mcp.md](./mcp.md), [skills-rules.md](./skills-rules.md), [personal-knowledge-base.md](./personal-knowledge-base.md)
