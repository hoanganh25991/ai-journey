#!/usr/bin/env python3
"""Generate missing AI Lab slide decks (Neural Ledger style) + SVG diagrams."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLIDES = ROOT / "slides"
ASSETS = SLIDES / "assets"

SHELL = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&family=Sora:wght@400;600;700&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="../_shared/deck.css" />
<style>
.shot {{
  width: 100%; height: 420px; object-fit: contain; border-radius: 14px;
  border: 1px solid var(--line); background: #e6edf5;
}}
.shot-lg {{ height: 520px; }}
.shot-md {{ height: 380px; }}
.mini {{ font-size: 18px !important; }}
.table-card {{ overflow: hidden; }}
.table-card table {{ width: 100%; border-collapse: collapse; font-size: 18px; }}
.table-card th, .table-card td {{
  text-align: left; padding: 12px 14px; border-bottom: 1px solid var(--line);
  color: var(--muted); vertical-align: top;
}}
.table-card th {{ color: var(--ink); font-family: var(--font-mono); font-size: 14px;
  letter-spacing: 0.06em; text-transform: uppercase; }}
.code-block {{
  font-family: var(--font-mono); font-size: 18px; line-height: 1.55;
  background: rgba(22,32,46,0.92); color: #e8eef7; padding: 24px 28px;
  border-radius: 14px; white-space: pre; overflow: hidden;
}}
.code-block .c {{ color: #8b97a8; }}
.code-block .k {{ color: #5ec8d4; }}
.code-block .s {{ color: #f0a35e; }}
</style>
</head>
<body>
<div class="deck-viewport">
<main class="deck-stage" id="deckStage">
{body}
</main>
</div>
<nav class="deck-controls">
  <button type="button" id="prevBtn">←</button>
  <span id="pageLabel">1</span>
  <button type="button" id="nextBtn">→</button>
</nav>
<script src="../_shared/deck.js"></script>
</body>
</html>
"""


def slide(inner: str, n: str, foot: str) -> str:
    return f"""
<section class="slide">
  <div class="slide-bg"></div><div class="grid-overlay"></div>
  <div class="pad">
{inner}
  </div>
  <div class="foot"><span>{n}</span><span>{foot}</span></div>
</section>
"""


def title_slide(
    eyebrow: str,
    pill: str,
    h1: str,
    lead: str,
    steps: list[str],
    n: str = "01",
    foot: str = "AI Lab",
) -> str:
    flow = "".join(
        f'<span class="step">{s}</span>'
        + (f'<span class="arr">→</span>' if i < len(steps) - 1 else "")
        for i, s in enumerate(steps)
    )
    return slide(
        f"""    <div class="topbar reveal"><span>{eyebrow}</span><span class="pill">{pill}</span></div>
    <h1 class="reveal" style="margin-top:72px;">{h1}</h1>
    <p class="lead reveal" style="margin-top:28px;">{lead}</p>
    <div class="flow-row reveal">{flow}</div>""",
        n,
        foot,
    ).replace('class="slide"', 'class="slide active"', 1)


def ideas_slide(topic: str, note: str, cards: list[tuple[str, str, str]], n: str, keywords: str) -> str:
    cols = "".join(
        f'<div class="card {"cyan " if i % 2 else ""}reveal"><div class="tag">{tag}</div><h3>{h}</h3><p>{p}</p></div>'
        for i, (tag, h, p) in enumerate(cards)
    )
    grid = "cols-3" if len(cards) >= 3 else "cols-2"
    return slide(
        f"""    <div class="topbar reveal"><span>{topic}</span><span class="pill">ideas</span></div>
    <h2 class="reveal">Key ideas</h2>
    <div class="{grid}">{cols}</div>
    <p class="lead reveal" style="margin-top:24px;font-size:20px;">Keywords: {keywords} · Read: <span style="color:var(--amber);font-family:var(--font-mono)">{note}</span></p>""",
        n,
        note,
    )


def img_slide(label: str, src: str, alt: str, n: str, caption: str = "") -> str:
    cap = f'<p class="lead reveal" style="margin-top:12px;font-size:20px;">{caption}</p>' if caption else ""
    return slide(
        f"""    <div class="topbar reveal"><span>Illustration</span><span class="pill">{label}</span></div>
    <h2 class="reveal" style="font-size:36px;margin-bottom:16px;">Illustration</h2>
    <img class="shot shot-lg reveal" src="{src}" alt="{alt}" />
    {cap}""",
        n,
        "AI Lab · illustration",
    )


def cards_slide(topic: str, pill: str, h2: str, cards: list[tuple[str, str, str]], n: str, foot: str) -> str:
    cols = "".join(
        f'<div class="card {"cyan " if i % 2 else ""}{"accent " if i == 0 and len(cards)==3 else ""}reveal"><div class="tag">{tag}</div><h3>{h}</h3><p>{p}</p></div>'
        for i, (tag, h, p) in enumerate(cards)
    )
    grid = "cols-3" if len(cards) == 3 else "cols-2"
    return slide(
        f"""    <div class="topbar reveal"><span>{topic}</span><span class="pill">{pill}</span></div>
    <h2 class="reveal">{h2}</h2>
    <div class="{grid}">{cols}</div>""",
        n,
        foot,
    )


def table_slide(topic: str, pill: str, h2: str, headers: list[str], rows: list[list[str]], n: str, foot: str) -> str:
    th = "".join(f"<th>{h}</th>" for h in headers)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return slide(
        f"""    <div class="topbar reveal"><span>{topic}</span><span class="pill">{pill}</span></div>
    <h2 class="reveal">{h2}</h2>
    <div class="card table-card reveal">
      <table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>
    </div>""",
        n,
        foot,
    )


def code_slide(topic: str, pill: str, h2: str, code: str, n: str, foot: str, side: str = "") -> str:
    if side:
        body = f"""    <div class="topbar reveal"><span>{topic}</span><span class="pill">{pill}</span></div>
    <h2 class="reveal">{h2}</h2>
    <div class="cols-2">
      <div class="code-block reveal">{code}</div>
      <div class="card cyan reveal">{side}</div>
    </div>"""
    else:
        body = f"""    <div class="topbar reveal"><span>{topic}</span><span class="pill">{pill}</span></div>
    <h2 class="reveal">{h2}</h2>
    <div class="code-block reveal">{code}</div>"""
    return slide(body, n, foot)


def pipeline_slide(topic: str, h2: str, steps: list[str], n: str, foot: str, note: str = "") -> str:
    flow = "".join(
        f'<span class="step">{s}</span>'
        + (f'<span class="arr">→</span>' if i < len(steps) - 1 else "")
        for i, s in enumerate(steps)
    )
    extra = f'<p class="lead reveal" style="margin-top:36px;">{note}</p>' if note else ""
    return slide(
        f"""    <div class="topbar reveal"><span>{topic}</span><span class="pill">pipeline</span></div>
    <h2 class="reveal">{h2}</h2>
    <div class="flow-row reveal" style="margin-top:48px;">{flow}</div>
    {extra}""",
        n,
        foot,
    )


def close_slide(
    h1: str,
    lead: str,
    cta_href: str | None = None,
    cta_label: str = "Open →",
    n: str = "end",
    foot: str = "AI Lab",
) -> str:
    cta = (
        f'<a class="app-cta reveal" href="{cta_href}">{cta_label}</a>'
        if cta_href
        else f'<a class="app-cta reveal" href="../../index.html">Back to hub →</a>'
    )
    return slide(
        f"""    <div class="topbar reveal"><span>Next</span><span class="pill">continue</span></div>
    <h1 class="reveal" style="margin-top:100px;font-size:64px;">{h1}</h1>
    <p class="lead reveal" style="margin-top:28px;">{lead}</p>
    {cta}""",
        n,
        foot,
    )


# --------------------------------------------------------------------------- #
# SVG diagrams                                                                 #
# --------------------------------------------------------------------------- #
SVG_CSS = dict(
    bg="#0c1118",
    card="#15202e",
    ink="#e8eef7",
    muted="#8b97a8",
    amber="#f0a35e",
    cyan="#5ec8d4",
)


def svg_box(x, y, w, h, label, stroke, sub=""):
    t1 = f'<text x="{x+w/2}" y="{y+h/2+(4 if not sub else -4)}" text-anchor="middle" fill="{SVG_CSS["ink"]}" font-family="IBM Plex Mono, monospace" font-size="14">{label}</text>'
    t2 = (
        f'<text x="{x+w/2}" y="{y+h/2+16}" text-anchor="middle" fill="{SVG_CSS["muted"]}" font-family="IBM Plex Mono, monospace" font-size="11">{sub}</text>'
        if sub
        else ""
    )
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{SVG_CSS["card"]}" stroke="{stroke}" stroke-width="2"/>{t1}{t2}'


def write_svgs() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)

    # classification pipeline
    (ASSETS / "classification-pipeline.svg").write_text(
        f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 540" fill="none">
  <rect width="960" height="540" fill="{SVG_CSS['bg']}"/>
  <defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="{SVG_CSS['amber']}"/></marker></defs>
  {svg_box(40, 220, 140, 70, "input", SVG_CSS["amber"], "text / image")}
  {svg_box(220, 220, 150, 70, "embedding", SVG_CSS["cyan"], "vector")}
  {svg_box(410, 220, 160, 70, "class head", SVG_CSS["amber"], "logits")}
  {svg_box(610, 220, 140, 70, "softmax", SVG_CSS["cyan"], "probs")}
  {svg_box(790, 220, 130, 70, "label", SVG_CSS["amber"], "argmax")}
  <line x1="180" y1="255" x2="220" y2="255" stroke="{SVG_CSS['amber']}" stroke-width="2" marker-end="url(#a)"/>
  <line x1="370" y1="255" x2="410" y2="255" stroke="{SVG_CSS['cyan']}" stroke-width="2" marker-end="url(#a)"/>
  <line x1="570" y1="255" x2="610" y2="255" stroke="{SVG_CSS['amber']}" stroke-width="2" marker-end="url(#a)"/>
  <line x1="750" y1="255" x2="790" y2="255" stroke="{SVG_CSS['cyan']}" stroke-width="2" marker-end="url(#a)"/>
  <text x="480" y="120" text-anchor="middle" fill="{SVG_CSS['ink']}" font-family="Sora, sans-serif" font-size="28">Classification pipeline</text>
  <text x="480" y="400" text-anchor="middle" fill="{SVG_CSS['muted']}" font-family="IBM Plex Mono, monospace" font-size="14">train with cross-entropy · evaluate with F1 on imbalanced data</text>
</svg>
""",
        encoding="utf-8",
    )

    # train-infer
    (ASSETS / "train-infer-flow.svg").write_text(
        f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 540" fill="none">
  <rect width="960" height="540" fill="{SVG_CSS['bg']}"/>
  {svg_box(60, 160, 360, 220, "", SVG_CSS["amber"])}
  <text x="240" y="220" text-anchor="middle" fill="{SVG_CSS['amber']}" font-family="IBM Plex Mono, monospace" font-size="16">TRAIN</text>
  <text x="240" y="260" text-anchor="middle" fill="{SVG_CSS['ink']}" font-family="Sora, sans-serif" font-size="22">many GPU epochs</text>
  <text x="240" y="300" text-anchor="middle" fill="{SVG_CSS['muted']}" font-family="IBM Plex Mono, monospace" font-size="14">data → loss → update weights</text>
  <text x="240" y="340" text-anchor="middle" fill="{SVG_CSS['muted']}" font-family="IBM Plex Mono, monospace" font-size="14">output: checkpoint</text>
  {svg_box(540, 160, 360, 220, "", SVG_CSS["cyan"])}
  <text x="720" y="220" text-anchor="middle" fill="{SVG_CSS['cyan']}" font-family="IBM Plex Mono, monospace" font-size="16">INFERENCE</text>
  <text x="720" y="260" text-anchor="middle" fill="{SVG_CSS['ink']}" font-family="Sora, sans-serif" font-size="22">light realtime</text>
  <text x="720" y="300" text-anchor="middle" fill="{SVG_CSS['muted']}" font-family="IBM Plex Mono, monospace" font-size="14">load weights → predict</text>
  <text x="720" y="340" text-anchor="middle" fill="{SVG_CSS['muted']}" font-family="IBM Plex Mono, monospace" font-size="14">output: label / action</text>
  <path d="M430 270 H530" stroke="{SVG_CSS['ink']}" stroke-width="2" marker-end="url(#a)"/>
  <defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="{SVG_CSS['ink']}"/></marker></defs>
  <text x="480" y="80" text-anchor="middle" fill="{SVG_CSS['ink']}" font-family="Sora, sans-serif" font-size="28">Two lives of a model</text>
</svg>
""",
        encoding="utf-8",
    )

    # semantic hybrid
    (ASSETS / "semantic-hybrid.svg").write_text(
        f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 540" fill="none">
  <rect width="960" height="540" fill="{SVG_CSS['bg']}"/>
  <defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="{SVG_CSS['amber']}"/></marker></defs>
  {svg_box(380, 40, 200, 56, "question", SVG_CSS["ink"])}
  {svg_box(80, 180, 280, 80, "Inverted index", SVG_CSS["amber"], "BM25 / Elastic · fast")}
  {svg_box(600, 180, 280, 80, "Semantic index", SVG_CSS["cyan"], "embeddings · meaning")}
  {svg_box(300, 360, 360, 80, "merge / rerank → top-k", SVG_CSS["amber"], "Hybrid · Tiered · Fallback")}
  <line x1="420" y1="96" x2="220" y2="180" stroke="{SVG_CSS['amber']}" stroke-width="1.5" marker-end="url(#a)"/>
  <line x1="540" y1="96" x2="740" y2="180" stroke="{SVG_CSS['cyan']}" stroke-width="1.5" marker-end="url(#a)"/>
  <line x1="220" y1="260" x2="400" y2="360" stroke="{SVG_CSS['amber']}" stroke-width="1.5" marker-end="url(#a)"/>
  <line x1="740" y1="260" x2="560" y2="360" stroke="{SVG_CSS['cyan']}" stroke-width="1.5" marker-end="url(#a)"/>
  <text x="480" y="500" text-anchor="middle" fill="{SVG_CSS['muted']}" font-family="IBM Plex Mono, monospace" font-size="13">keyword filter + meaning rank = pragmatic semantic search</text>
</svg>
""",
        encoding="utf-8",
    )

    # vector db
    (ASSETS / "vector-db-flow.svg").write_text(
        f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 540" fill="none">
  <rect width="960" height="540" fill="{SVG_CSS['bg']}"/>
  <defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="{SVG_CSS['cyan']}"/></marker></defs>
  {svg_box(40, 120, 180, 70, "documents", SVG_CSS["amber"])}
  {svg_box(260, 120, 140, 70, "chunk", SVG_CSS["cyan"])}
  {svg_box(440, 120, 160, 70, "embed", SVG_CSS["amber"])}
  {svg_box(640, 100, 280, 110, "vector DB", SVG_CSS["cyan"], "ANN · metadata · CRUD")}
  {svg_box(40, 340, 180, 70, "question", SVG_CSS["amber"])}
  {svg_box(260, 340, 160, 70, "embed", SVG_CSS["cyan"])}
  {svg_box(460, 340, 200, 70, "top-k search", SVG_CSS["amber"])}
  {svg_box(700, 340, 200, 70, "RAG / search", SVG_CSS["cyan"])}
  <line x1="220" y1="155" x2="260" y2="155" stroke="{SVG_CSS['amber']}" stroke-width="2" marker-end="url(#a)"/>
  <line x1="400" y1="155" x2="440" y2="155" stroke="{SVG_CSS['cyan']}" stroke-width="2" marker-end="url(#a)"/>
  <line x1="600" y1="155" x2="640" y2="155" stroke="{SVG_CSS['amber']}" stroke-width="2" marker-end="url(#a)"/>
  <line x1="220" y1="375" x2="260" y2="375" stroke="{SVG_CSS['amber']}" stroke-width="2" marker-end="url(#a)"/>
  <line x1="420" y1="375" x2="460" y2="375" stroke="{SVG_CSS['cyan']}" stroke-width="2" marker-end="url(#a)"/>
  <line x1="660" y1="375" x2="700" y2="375" stroke="{SVG_CSS['amber']}" stroke-width="2" marker-end="url(#a)"/>
  <text x="480" y="60" text-anchor="middle" fill="{SVG_CSS['ink']}" font-family="Sora, sans-serif" font-size="26">Index once · query many times</text>
</svg>
""",
        encoding="utf-8",
    )

    # skills layers
    (ASSETS / "skills-layers.svg").write_text(
        f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 540" fill="none">
  <rect width="960" height="540" fill="{SVG_CSS['bg']}"/>
  {svg_box(80, 80, 240, 380, "", SVG_CSS["amber"])}
  <text x="200" y="140" text-anchor="middle" fill="{SVG_CSS['amber']}" font-family="IBM Plex Mono, monospace" font-size="15">SKILL</text>
  <text x="200" y="190" text-anchor="middle" fill="{SVG_CSS['ink']}" font-family="Sora, sans-serif" font-size="18">packaged know-how</text>
  <text x="200" y="240" text-anchor="middle" fill="{SVG_CSS['muted']}" font-family="IBM Plex Mono, monospace" font-size="13">SKILL.md + scripts</text>
  <text x="200" y="280" text-anchor="middle" fill="{SVG_CSS['muted']}" font-family="IBM Plex Mono, monospace" font-size="13">loaded when needed</text>
  <text x="200" y="340" text-anchor="middle" fill="{SVG_CSS['muted']}" font-family="IBM Plex Mono, monospace" font-size="13">graphify · slides</text>
  {svg_box(360, 80, 240, 380, "", SVG_CSS["cyan"])}
  <text x="480" y="140" text-anchor="middle" fill="{SVG_CSS['cyan']}" font-family="IBM Plex Mono, monospace" font-size="15">RULE</text>
  <text x="480" y="190" text-anchor="middle" fill="{SVG_CSS['ink']}" font-family="Sora, sans-serif" font-size="18">always-on constraint</text>
  <text x="480" y="240" text-anchor="middle" fill="{SVG_CSS['muted']}" font-family="IBM Plex Mono, monospace" font-size="13">always or glob</text>
  <text x="480" y="280" text-anchor="middle" fill="{SVG_CSS['muted']}" font-family="IBM Plex Mono, monospace" font-size="13">keep short</text>
  <text x="480" y="340" text-anchor="middle" fill="{SVG_CSS['muted']}" font-family="IBM Plex Mono, monospace" font-size="13">commit · notes-first</text>
  {svg_box(640, 80, 240, 380, "", SVG_CSS["amber"])}
  <text x="760" y="140" text-anchor="middle" fill="{SVG_CSS['amber']}" font-family="IBM Plex Mono, monospace" font-size="15">COMMAND</text>
  <text x="760" y="190" text-anchor="middle" fill="{SVG_CSS['ink']}" font-family="Sora, sans-serif" font-size="18">user shortcut</text>
  <text x="760" y="240" text-anchor="middle" fill="{SVG_CSS['muted']}" font-family="IBM Plex Mono, monospace" font-size="13">typed by user</text>
  <text x="760" y="280" text-anchor="middle" fill="{SVG_CSS['muted']}" font-family="IBM Plex Mono, monospace" font-size="13">/deep-plan · /loop</text>
  <text x="480" y="500" text-anchor="middle" fill="{SVG_CSS['muted']}" font-family="IBM Plex Mono, monospace" font-size="13">home: ~/.agents/skills — write once, use across clients</text>
</svg>
""",
        encoding="utf-8",
    )

    # timeline strip
    (ASSETS / "ai-timeline-strip.svg").write_text(
        f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 540" fill="none">
  <rect width="960" height="540" fill="{SVG_CSS['bg']}"/>
  <line x1="80" y1="270" x2="880" y2="270" stroke="{SVG_CSS['cyan']}" stroke-width="3"/>
  <g font-family="IBM Plex Mono, monospace">
    <circle cx="140" cy="270" r="10" fill="{SVG_CSS['amber']}"/>
    <text x="140" y="220" text-anchor="middle" fill="{SVG_CSS['ink']}" font-size="16">2023</text>
    <text x="140" y="320" text-anchor="middle" fill="{SVG_CSS['muted']}" font-size="12">LLM basics</text>
    <text x="140" y="340" text-anchor="middle" fill="{SVG_CSS['muted']}" font-size="12">tokenize→RAG</text>
    <circle cx="340" cy="270" r="10" fill="{SVG_CSS['cyan']}"/>
    <text x="340" y="220" text-anchor="middle" fill="{SVG_CSS['ink']}" font-size="16">2024</text>
    <text x="340" y="320" text-anchor="middle" fill="{SVG_CSS['muted']}" font-size="12">coding agents</text>
    <text x="340" y="340" text-anchor="middle" fill="{SVG_CSS['muted']}" font-size="12">Claude 3.5</text>
    <circle cx="540" cy="270" r="12" fill="{SVG_CSS['amber']}"/>
    <text x="540" y="200" text-anchor="middle" fill="{SVG_CSS['amber']}" font-size="16">Nov 2024</text>
    <text x="540" y="320" text-anchor="middle" fill="{SVG_CSS['ink']}" font-size="13">MCP hinge</text>
    <text x="540" y="340" text-anchor="middle" fill="{SVG_CSS['muted']}" font-size="12">tools for agents</text>
    <circle cx="720" cy="270" r="10" fill="{SVG_CSS['cyan']}"/>
    <text x="720" y="220" text-anchor="middle" fill="{SVG_CSS['ink']}" font-size="16">2025</text>
    <text x="720" y="320" text-anchor="middle" fill="{SVG_CSS['muted']}" font-size="12">harness · skills</text>
    <circle cx="860" cy="270" r="10" fill="{SVG_CSS['amber']}"/>
    <text x="860" y="220" text-anchor="middle" fill="{SVG_CSS['ink']}" font-size="16">2026</text>
    <text x="860" y="320" text-anchor="middle" fill="{SVG_CSS['muted']}" font-size="12">Grok 4.5</text>
    <text x="860" y="340" text-anchor="middle" fill="{SVG_CSS['muted']}" font-size="12">automation</text>
  </g>
  <text x="480" y="80" text-anchor="middle" fill="{SVG_CSS['ink']}" font-family="Sora, sans-serif" font-size="28">Understanding models → steering agents</text>
</svg>
""",
        encoding="utf-8",
    )

    # pytorch loop svg
    (ASSETS / "pytorch-steps.svg").write_text(
        f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 540" fill="none">
  <rect width="960" height="540" fill="{SVG_CSS['bg']}"/>
  <defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="{SVG_CSS['amber']}"/></marker></defs>
  {svg_box(80, 200, 160, 100, "1 · forward", SVG_CSS["amber"], "logits = model(x)")}
  {svg_box(290, 200, 160, 100, "2 · loss", SVG_CSS["cyan"], "vs labels")}
  {svg_box(500, 200, 160, 100, "3 · backward", SVG_CSS["amber"], "gradients")}
  {svg_box(710, 200, 160, 100, "4 · step", SVG_CSS["cyan"], "update W")}
  <line x1="240" y1="250" x2="290" y2="250" stroke="{SVG_CSS['amber']}" stroke-width="2" marker-end="url(#a)"/>
  <line x1="450" y1="250" x2="500" y2="250" stroke="{SVG_CSS['cyan']}" stroke-width="2" marker-end="url(#a)"/>
  <line x1="660" y1="250" x2="710" y2="250" stroke="{SVG_CSS['amber']}" stroke-width="2" marker-end="url(#a)"/>
  <path d="M790 300 C790 400 160 400 160 300" stroke="{SVG_CSS['muted']}" stroke-width="1.5" fill="none" stroke-dasharray="6 4"/>
  <text x="480" y="420" text-anchor="middle" fill="{SVG_CSS['muted']}" font-family="IBM Plex Mono, monospace" font-size="13">zero_grad() each batch · many epochs</text>
  <text x="480" y="100" text-anchor="middle" fill="{SVG_CSS['ink']}" font-family="Sora, sans-serif" font-size="28">PyTorch batch loop</text>
</svg>
""",
        encoding="utf-8",
    )


# --------------------------------------------------------------------------- #
# Decks                                                                       #
# --------------------------------------------------------------------------- #


def deck_classification() -> str:
    body = "".join(
        [
            title_slide(
                "Concept · classification",
                "teaching",
                "Classification · <em>label the input</em>",
                "Given text, image, or numbers — pick one label from a fixed set. The most common model-building task after softmax.",
                ["input", "embedding", "head", "softmax", "label"],
            ),
            cards_slide(
                "Why",
                "matters",
                "Why classification shows up everywhere",
                [
                    ("review", "Sentiment", "Is this review positive or negative?"),
                    ("inbox", "Spam filter", "Email spam / not spam — binary decisions."),
                    ("route", "Easy vs hard", "Route questions by difficulty before calling a big model."),
                ],
                "02",
                "notes/classification.md",
            ),
            ideas_slide(
                "Classification",
                "notes/classification.md",
                [
                    ("head", "Classification head", "Last layer → logits per label → softmax → pick the highest."),
                    ("kinds", "Binary / multi / multi-label", "Two classes · exactly one of many · several labels at once."),
                    ("loss", "Cross-entropy", "Measures how wrong the predicted probability is; training pushes it down."),
                ],
                "03",
                "classification · cross-entropy · multi-class · F1",
            ),
            img_slide("classification-hero.png", "../assets/classification-hero.png", "Classification hero", "04", "Scores become a discrete decision."),
            img_slide("classification-pipeline.svg", "../assets/classification-pipeline.svg", "Pipeline", "05"),
            img_slide("softmax-regression.jpg", "../../notes/assets/protonx/softmax-regression.jpg", "Softmax regression", "06", "Multi-class classification model."),
            img_slide("softmax.jpg", "../../notes/assets/protonx/softmax.jpg", "Softmax", "07", "Raw scores → probabilities that sum to 1."),
            table_slide(
                "Evaluate",
                "metrics",
                "Accuracy is easy — and often misleading",
                ["Metric", "Asks", "Watch out"],
                [
                    ["Accuracy", "How often correct?", "Fails on imbalanced classes"],
                    ["Precision", "Of predicted positives, how many true?", "False alarms"],
                    ["Recall", "Of true positives, how many found?", "Missed rare labels"],
                    ["F1", "Harmonic mean of P & R", "Better default on skewed data"],
                ],
                "08",
                "notes/classification.md",
            ),
            cards_slide(
                "Pitfalls",
                "watch",
                "Easy to go wrong",
                [
                    ("balance", "Class imbalance", "Rare labels get ignored — inspect the label distribution first."),
                    ("leak", "Train/val leak", "Same examples in train and val → fake high scores."),
                    ("metric", "Wrong metric", "Optimizing accuracy on 95% majority class hides failure."),
                ],
                "09",
                "notes/classification.md",
            ),
            pipeline_slide(
                "Pipeline",
                "From input to label",
                ["input", "embed", "head", "softmax", "label"],
                "10",
                "train: cross-entropy",
                "Train with pytorch-training.md or tensorflow-training.md.",
            ),
            cards_slide(
                "Related",
                "next",
                "Where to go next",
                [
                    ("before", "Softmax", "How scores become probabilities."),
                    ("train", "PyTorch / TensorFlow", "Actually run the training loop."),
                    ("demo", "Sentiment / car-nn", "See classification in a browser demo."),
                ],
                "11",
                "related notes",
            ),
            close_slide(
                "Read the note<br /><em>then train it.</em>",
                "notes/classification.md — then pytorch-training or tensorflow-training.",
                "../../notes/classification.html",
                "Open note →",
            ),
        ]
    )
    return SHELL.format(title="Classification · slides", body=body)


def deck_pytorch() -> str:
    code = """<span class="k">for</span> epoch <span class="k">in</span> range(EPOCHS):
    <span class="k">for</span> x, y <span class="k">in</span> dataloader:
        opt.zero_grad()
        logits = model(x)       <span class="c"># forward</span>
        loss = loss_fn(logits, y)
        loss.backward()         <span class="c"># gradients</span>
        opt.step()              <span class="c"># update W</span>"""
    body = "".join(
        [
            title_slide(
                "Concept · pytorch-training",
                "teaching",
                "Train with <em>PyTorch</em>",
                "Epoch loop you write yourself: forward → loss → backward → step until the model is good enough.",
                ["dataset", "DataLoader", "epoch loop", "checkpoint"],
            ),
            cards_slide(
                "Why",
                "matters",
                "Why learn the loop by hand",
                [
                    ("flex", "Most flexible", "You see exactly how learning happens — what high-level APIs wrap."),
                    ("same", "Same mechanism", "Hugging Face Trainer and sentence-transformers sit on this loop."),
                    ("debug", "Debuggable", "When loss explodes, you know which step to inspect."),
                ],
                "02",
                "notes/pytorch-training.md",
            ),
            ideas_slide(
                "PyTorch",
                "notes/pytorch-training.md",
                [
                    ("batch", "Epoch vs batch", "Epoch = one pass over all data; batch = chunk processed per step."),
                    ("four", "Four steps", "forward → loss → backward() → step(). Always zero_grad()."),
                    ("lr", "Optimizer + LR", "Adam/SGD; LR too high → jumps; too low → crawls."),
                ],
                "03",
                "pytorch · epoch · optimizer · backprop",
            ),
            img_slide("pytorch-loop.png", "../assets/pytorch-loop.png", "Training loop", "04"),
            img_slide("pytorch-steps.svg", "../assets/pytorch-steps.svg", "Four steps", "05"),
            code_slide(
                "Code",
                "skeleton",
                "The batch loop",
                code,
                "06",
                "notes/pytorch-training.md",
                side='<div class="tag">remember</div><h3>zero_grad()</h3><p>Without clearing gradients, updates accumulate across batches and training goes wild.</p>',
            ),
            cards_slide(
                "Validate",
                "overfit",
                "Train vs validation",
                [
                    ("split", "Hold out val", "Track val loss every epoch — not just train loss."),
                    ("overfit", "Overfitting", "Train loss ↓ while val loss ↑ → memorizing, not generalizing."),
                    ("save", "Checkpoint", "torch.save(model.state_dict()) for inference later."),
                ],
                "07",
                "notes/pytorch-training.md",
            ),
            cards_slide(
                "GPU",
                "speed",
                "Move model and batch to device",
                [
                    ("cuda", ".to(\"cuda\")", "Model and each batch must live on the same device."),
                    ("note", "train-gpu.md", "Full stack: HF/Kaggle data + Colab/cloud notebooks."),
                    ("export", "Then infer", "Training is heavy once; inference is light forever."),
                ],
                "08",
                "notes/train-gpu.md",
            ),
            pipeline_slide(
                "Pipeline",
                "Dataset → checkpoint",
                ["dataset", "DataLoader", "forward", "loss", "backward", "step", "ckpt"],
                "09",
                "notes/pytorch-training.md",
            ),
            cards_slide(
                "Compare",
                "vs TF",
                "PyTorch vs TensorFlow style",
                [
                    ("pt", "PyTorch", "You write the loop — maximum control."),
                    ("tf", "Keras", "compile + fit — framework runs the loop."),
                    ("pick", "Choose by project", "Same learning idea; different API ergonomics."),
                ],
                "10",
                "related",
            ),
            close_slide(
                "Write the loop<br /><em>once.</em>",
                "notes/pytorch-training.md — then try tensorflow-training for the declarative twin.",
                "../../notes/pytorch-training.html",
                "Open note →",
            ),
        ]
    )
    return SHELL.format(title="PyTorch training · slides", body=body)


def deck_tensorflow() -> str:
    code = """model = keras.Sequential([
  Dense(64, activation=<span class="s">"relu"</span>),
  Dense(NUM_CLASSES, activation=<span class="s">"softmax"</span>),
])
model.compile(optimizer=<span class="s">"adam"</span>,
  loss=<span class="s">"sparse_categorical_crossentropy"</span>,
  metrics=[<span class="s">"accuracy"</span>])
model.fit(x, y, epochs=EPOCHS, validation_data=val)"""
    body = "".join(
        [
            title_slide(
                "Concept · tensorflow-training",
                "teaching",
                "Train with <em>TensorFlow / Keras</em>",
                "Same classifier lesson, declarative style: define the model, compile, then fit over epochs.",
                ["dataset", "model", "compile", "fit", "checkpoint"],
            ),
            cards_slide(
                "Why",
                "matters",
                "Why Keras still matters",
                [
                    ("short", "Concise", "No manual backward/step — the framework owns the loop."),
                    ("viz", "Projector", "Embedding Projector makes vector space visible in 3D."),
                    ("pair", "Pair with PyTorch", "Two APIs, one learning idea — pick what fits."),
                ],
                "02",
                "notes/tensorflow-training.md",
            ),
            ideas_slide(
                "Keras",
                "notes/tensorflow-training.md",
                [
                    ("compile", "compile = how to learn", "Optimizer, loss (cross-entropy), metrics."),
                    ("fit", "fit = run training", "Epochs, batches, backprop — handled for you."),
                    ("cb", "Callbacks", "EarlyStopping + ModelCheckpoint save the best model."),
                ],
                "03",
                "tensorflow · keras · epoch",
            ),
            img_slide("tensorflow-keras.png", "../assets/tensorflow-keras.png", "Keras flow", "04"),
            code_slide("Code", "skeleton", "compile then fit", code, "05", "notes/tensorflow-training.md"),
            img_slide("softmax-regression.jpg", "../../notes/assets/protonx/softmax-regression.jpg", "Softmax regression", "06"),
            img_slide("tf-projector.jpg", "../../notes/assets/protonx/tf-projector.jpg", "Embedding Projector", "07", "Inspect embeddings in 3D while training."),
            cards_slide(
                "Monitor",
                "curves",
                "What to watch each epoch",
                [
                    ("acc", "accuracy", "Rising on train — good, but not enough alone."),
                    ("val", "val_loss", "Rising while train falls → overfitting."),
                    ("stop", "EarlyStopping", "Stop when val stops improving; keep best weights."),
                ],
                "08",
                "notes/tensorflow-training.md",
            ),
            pipeline_slide(
                "Pipeline",
                "Same destination as PyTorch",
                ["dataset", "Keras model", "compile", "fit", "checkpoint"],
                "09",
                "serves classification.md",
            ),
            cards_slide(
                "Related",
                "stack",
                "Connect the stack",
                [
                    ("cls", "Classification", "The task this trains."),
                    ("pt", "PyTorch twin", "Manual loop version of the same idea."),
                    ("emb", "Embedding", "Projector visualizes the vectors."),
                ],
                "10",
                "related",
            ),
            close_slide(
                "Declare it,<br /><em>then fit.</em>",
                "notes/tensorflow-training.md",
                "../../notes/tensorflow-training.html",
                "Open note →",
            ),
        ]
    )
    return SHELL.format(title="TensorFlow training · slides", body=body)


def deck_huggingface() -> str:
    body = "".join(
        [
            title_slide(
                "Concept · huggingface",
                "teaching",
                "Hugging Face · <em>dataset + Space</em>",
                "GitHub for AI: Datasets, pretrained Models, and Spaces — shorten the path from idea to a usable model.",
                ["Datasets", "Hub model", "fine-tune", "Spaces"],
            ),
            cards_slide(
                "Why",
                "matters",
                "Standing on others' work",
                [
                    ("cost", "Scratch is expensive", "Pretrained + light fine-tune beats training from zero."),
                    ("data", "Labeled data ready", "load_dataset(...) — one line to a training set."),
                    ("share", "Demo in minutes", "Spaces host Gradio/Streamlit with optional GPU."),
                ],
                "02",
                "notes/huggingface.md",
            ),
            ideas_slide(
                "Hub",
                "notes/huggingface.md",
                [
                    ("data", "Datasets", "Labeled corpora ready for Trainer or your own loop."),
                    ("models", "Models", "BERT, GPT, ViT… fine-tune instead of scratch."),
                    ("spaces", "Spaces", "Push a demo → UI + API endpoint."),
                ],
                "03",
                "huggingface · datasets · spaces · fine-tune",
            ),
            img_slide("huggingface-hub.png", "../assets/huggingface-hub.png", "Three pillars", "04"),
            cards_slide(
                "Workflow",
                "path",
                "Typical fine-tune path",
                [
                    ("1", "Load data", "datasets.load_dataset(...)"),
                    ("2", "Load model", "transformers AutoModel + tokenizer"),
                    ("3", "Train", "Trainer API or PyTorch/TF loop"),
                    ("4", "Publish", "push to Hub / deploy Space"),
                ],
                "05",
                "notes/huggingface.md",
            ),
            cards_slide(
                "Fine-tune",
                "vs scratch",
                "Fine-tune beats scratch",
                [
                    ("less", "Less data", "Reuse knowledge from large pretraining."),
                    ("time", "Less time", "Hours instead of weeks on a GPU."),
                    ("card", "Read the card", "License + intended use before commercial work."),
                ],
                "06",
                "notes/huggingface.md",
            ),
            pipeline_slide(
                "Pipeline",
                "From Hub to use",
                ["HF Datasets", "pretrained", "fine-tune", "Hub / Spaces", "infer"],
                "07",
                "notes/huggingface.md",
            ),
            cards_slide(
                "Pair",
                "kaggle",
                "HF + Kaggle",
                [
                    ("hf", "Hugging Face", "Models + datasets + Spaces."),
                    ("kg", "Kaggle", "Free GPU notebooks + competitions."),
                    ("combo", "Often combined", "HF model + Kaggle GPU notebook."),
                ],
                "08",
                "related",
            ),
            cards_slide(
                "Pitfalls",
                "watch",
                "Before you ship",
                [
                    ("lic", "License", "Check commercial restrictions on the model card."),
                    ("tok", "Tokenizer match", "Always use the tokenizer that matches the model."),
                    ("leak", "Eval leak", "Don't fine-tune on your test set."),
                ],
                "09",
                "notes/huggingface.md",
            ),
            close_slide(
                "Borrow, fine-tune,<br /><em>share.</em>",
                "notes/huggingface.md — then kaggle.md for free GPU hours.",
                "../../notes/huggingface.html",
                "Open note →",
            ),
        ]
    )
    return SHELL.format(title="Hugging Face · slides", body=body)


def deck_kaggle() -> str:
    body = "".join(
        [
            title_slide(
                "Concept · kaggle",
                "teaching",
                "Kaggle · <em>dataset + GPU notebook</em>",
                "Free datasets, notebooks with GPU/TPU, and competitions — the hands-on twin of Hugging Face.",
                ["dataset", "notebook", "enable GPU", "train", "export"],
            ),
            cards_slide(
                "Why",
                "matters",
                "What learners usually lack",
                [
                    ("data", "Good data", "Tens of thousands of public datasets."),
                    ("compute", "Enough compute", "Free GPU/TPU hours in the browser."),
                    ("peers", "Public solutions", "Read top notebooks — learn faster."),
                ],
                "02",
                "notes/kaggle.md",
            ),
            ideas_slide(
                "Kaggle",
                "notes/kaggle.md",
                [
                    ("ds", "Datasets", "Download straight into a notebook."),
                    ("nb", "Notebooks", "Built-in libs; flip GPU on in settings."),
                    ("comp", "Competitions", "Metric + leaderboard + public kernels."),
                ],
                "03",
                "kaggle · dataset · gpu · competition",
            ),
            img_slide("kaggle-stack.png", "../assets/kaggle-stack.png", "Kaggle stack", "04"),
            cards_slide(
                "Quota",
                "limits",
                "Free GPU is capped",
                [
                    ("week", "Weekly hours", "Save GPU for real training runs, not idle kernels."),
                    ("tpu", "TPU option", "Useful for TF/Keras workloads."),
                    ("export", "Export model", "Download checkpoint → use in demos / Spaces."),
                ],
                "05",
                "notes/kaggle.md",
            ),
            pipeline_slide(
                "Pipeline",
                "Data → trained model",
                ["Kaggle dataset", "notebook + GPU", "train epochs", "export", "inference"],
                "06",
                "notes/kaggle.md",
            ),
            cards_slide(
                "Combo",
                "HF",
                "Classic combo",
                [
                    ("data", "Kaggle data", "Competition or public dataset."),
                    ("model", "HF pretrained", "Grab BERT / MiniLM from the Hub."),
                    ("run", "Train on Kaggle GPU", "No local CUDA install required."),
                ],
                "07",
                "notes/huggingface.md",
            ),
            cards_slide(
                "Practice",
                "comp",
                "How to learn from competitions",
                [
                    ("metric", "Read the metric", "Optimize what the leaderboard scores."),
                    ("public", "Public notebooks", "Reproduce a strong baseline first."),
                    ("iter", "Iterate small", "One change per submit — know what moved the score."),
                ],
                "08",
                "notes/kaggle.md",
            ),
            cards_slide(
                "Related",
                "stack",
                "In the training stack",
                [
                    ("gpu", "train-gpu.md", "Where this fits in the lab checklist."),
                    ("pt", "PyTorch / TF", "What you write inside the notebook."),
                    ("infer", "train-infer", "Export → plug into browser demos."),
                ],
                "09",
                "related",
            ),
            close_slide(
                "Enable GPU,<br /><em>then train.</em>",
                "notes/kaggle.md",
                "../../notes/kaggle.html",
                "Open note →",
            ),
        ]
    )
    return SHELL.format(title="Kaggle · slides", body=body)


def deck_transformer() -> str:
    body = "".join(
        [
            title_slide(
                "Concept · transformer",
                "teaching",
                "Transformer · <em>core LLM architecture</em>",
                "Stack attention blocks; process the whole sentence in parallel. The frame behind BERT, GPT, and modern LLMs.",
                ["tokens", "embed+pos", "N× attn+FFN", "head"],
            ),
            cards_slide(
                "Why",
                "2017",
                "Why Transformers won",
                [
                    ("rnn", "Before: RNN/LSTM", "Step-by-step — slow, forgets early context."),
                    ("par", "Parallel attend", "Every token attends to every other → GPU-friendly."),
                    ("era", "Opened LLMs", "Attention Is All You Need → BERT/GPT era."),
                ],
                "02",
                "notes/transformer.md",
            ),
            ideas_slide(
                "Transformer",
                "notes/transformer.md",
                [
                    ("stack", "Stacked blocks", "Multi-head attention + feed-forward, many layers."),
                    ("pos", "Positional encoding", "Parallel has no order — inject positions."),
                    ("ed", "Encoder / decoder", "BERT reads; GPT generates; both for MT."),
                ],
                "03",
                "transformer · attention · encoder · decoder",
            ),
            img_slide("transformer-stack.png", "../assets/transformer-stack.png", "Stacked blocks", "04"),
            img_slide("self-attention.jpg", "../../notes/assets/protonx/self-attention.jpg", "Self-attention", "05", "Inside one encoder block."),
            img_slide("cross-attention.jpg", "../../notes/assets/protonx/cross-attention.jpg", "Cross-attention", "06", "Decoder attends to encoder (translation)."),
            img_slide("attention-after-softmax.jpg", "../../notes/assets/protonx/attention-after-softmax.jpg", "After softmax", "07", "Attention weights inside a layer."),
            table_slide(
                "Roles",
                "variants",
                "Encoder · decoder · both",
                ["Kind", "Job", "Example"],
                [
                    ["Encoder", "Understand whole input", "BERT · classification · embeddings"],
                    ["Decoder", "Generate left → right", "GPT · chat · completion"],
                    ["Enc-Dec", "Map sequence → sequence", "Translation · summarization"],
                ],
                "08",
                "notes/transformer.md",
            ),
            cards_slide(
                "Stability",
                "tricks",
                "What keeps deep stacks trainable",
                [
                    ("res", "Residual links", "Skip connections keep gradients flowing."),
                    ("ln", "Layer norm", "Stabilizes activations across layers."),
                    ("gpu", "Parallel = fast", "No step dependency → full GPU use."),
                ],
                "09",
                "notes/transformer.md",
            ),
            pipeline_slide(
                "Pipeline",
                "Tokens to representation",
                ["tokens", "embed+pos", "N× (attn+FFN)", "head"],
                "10",
                "wraps attention · embedding · softmax",
            ),
            close_slide(
                "The house frame<br /><em>around attention.</em>",
                "notes/transformer.md — pretrained models live on Hugging Face.",
                "../../notes/transformer.html",
                "Open note →",
            ),
        ]
    )
    return SHELL.format(title="Transformer · slides", body=body)


def deck_sentence_transformers() -> str:
    code = """<span class="k">from</span> sentence_transformers <span class="k">import</span> SentenceTransformer, util
model = SentenceTransformer(<span class="s">"all-MiniLM-L6-v2"</span>)
emb = model.encode([<span class="s">"Hello"</span>, <span class="s">"Hi there"</span>])
sim = util.cos_sim(emb[0], emb[1])"""
    body = "".join(
        [
            title_slide(
                "Concept · sentence-transformers",
                "teaching",
                "sentence-transformers · <em>sentence vectors</em>",
                "Turn a whole sentence into a high-quality vector in a few lines — similarity and light classification without heavy training.",
                ["sentence", "encode()", "vector", "cos_sim / classify"],
            ),
            cards_slide(
                "Why",
                "matters",
                "Good embeddings, light stack",
                [
                    ("fast", "Minutes not weeks", "Pretrained MiniLM / mpnet ready via encode()."),
                    ("enough", "Often enough", "Vectors + logistic / k-NN beats fine-tuning a giant model."),
                    ("rag", "Feeds RAG", "Same vectors go into a vector DB for retrieve."),
                ],
                "02",
                "notes/sentence-transformers.md",
            ),
            ideas_slide(
                "SBERT",
                "notes/sentence-transformers.md",
                [
                    ("one", "One vector / sentence", "Optimized for sentence-level meaning, not per-token."),
                    ("sim", "Similarity", "cos_sim finds paraphrases and near neighbors."),
                    ("pick", "Pick a model", "MiniLM = fast; mpnet = more accurate."),
                ],
                "03",
                "sbert · embedding · similarity",
            ),
            img_slide("sentence-embed.png", "../assets/sentence-embed.png", "Sentence similarity", "04"),
            img_slide("cosine-similarity.jpg", "../../notes/assets/protonx/cosine-similarity.jpg", "Cosine", "05"),
            img_slide("embeddings-function.jpg", "../../notes/assets/protonx/embeddings-function.jpg", "Embedding function", "06"),
            code_slide("Code", "quick use", "encode → cos_sim", code, "07", "notes/sentence-transformers.md"),
            cards_slide(
                "Uses",
                "downstream",
                "What to do with the vectors",
                [
                    ("cls", "Light classifier", "Logistic / k-NN on top of embeddings."),
                    ("search", "Semantic search", "Rank documents by meaning."),
                    ("vdb", "Vector DB", "Index once; top-k forever."),
                ],
                "08",
                "related",
            ),
            pipeline_slide(
                "Pipeline",
                "Shortest path from text to meaning math",
                ["sentence", "encode", "vector", "cos_sim | classify | DB"],
                "09",
                "notes/sentence-transformers.md",
            ),
            close_slide(
                "encode()<br /><em>and ship.</em>",
                "notes/sentence-transformers.md → semantic-search / vector-database.",
                "../../notes/sentence-transformers.html",
                "Open note →",
            ),
        ]
    )
    return SHELL.format(title="sentence-transformers · slides", body=body)


def deck_vector_database() -> str:
    body = "".join(
        [
            title_slide(
                "Concept · vector-database",
                "teaching",
                "Vector database · <em>nearest neighbors fast</em>",
                "Store millions of embeddings and answer “closest to this?” in milliseconds — infrastructure under RAG and semantic search.",
                ["chunk", "embed", "index", "top-k"],
            ),
            cards_slide(
                "Why",
                "scale",
                "Why brute force dies",
                [
                    ("scan", "Linear scan", "Checking every vector is too slow at real scale."),
                    ("ann", "ANN indexes", "HNSW / IVF trade a little accuracy for huge speed."),
                    ("meta", "Metadata matters", "Filter by source/date/tags before or after search."),
                ],
                "02",
                "notes/vector-database.md",
            ),
            ideas_slide(
                "Vector DB",
                "notes/vector-database.md",
                [
                    ("nn", "Nearest neighbor", "Query vector → k closest by cosine or dot."),
                    ("ann", "Approximate", "Good enough for search; orders of magnitude faster."),
                    ("crud", "CRUD + filter", "Data changes; filters keep results relevant."),
                ],
                "03",
                "ANN · faiss · elasticsearch · pgvector",
            ),
            img_slide("vector-db-ann.png", "../assets/vector-db-ann.png", "ANN search", "04"),
            img_slide("vector-db-flow.svg", "../assets/vector-db-flow.svg", "Index + query", "05"),
            img_slide("embed-then-query.jpg", "../../notes/assets/protonx/embed-then-query.jpg", "Embed then query", "06"),
            img_slide("cosine-vs-dot.jpg", "../../notes/assets/protonx/cosine-vs-dot.jpg", "Cosine vs dot", "07"),
            table_slide(
                "Choices",
                "tools",
                "Pick by need",
                ["Tool", "Strength", "Gap"],
                [
                    ["FAISS", "In-memory speed", "No durable CRUD out of the box"],
                    ["Elasticsearch kNN", "Keyword + vector + scale", "Heavier ops"],
                    ["pgvector / Chroma", "Simple apps", "Not for huge distributed loads"],
                ],
                "08",
                "notes/vector-database.md",
            ),
            pipeline_slide(
                "Pipeline",
                "Documents in · answers out",
                ["docs", "chunk", "embed", "vector DB", "top-k", "RAG"],
                "09",
                "feeds rag.md · semantic-search.md",
            ),
            cards_slide(
                "Pitfalls",
                "watch",
                "Common failures",
                [
                    ("dim", "Dim mismatch", "Query encoder must match index encoder."),
                    ("stale", "Stale index", "Changed docs need re-embed + upsert."),
                    ("metric", "Wrong metric", "Cosine vs dot — ranking drifts if mismatched."),
                ],
                "10",
                "notes/vector-database.md",
            ),
            close_slide(
                "Index once,<br /><em>retrieve forever.</em>",
                "notes/vector-database.md",
                "../../notes/vector-database.html",
                "Open note →",
            ),
        ]
    )
    return SHELL.format(title="Vector database · slides", body=body)


def deck_semantic_search() -> str:
    body = "".join(
        [
            title_slide(
                "Project · semantic-search",
                "teaching",
                "Semantic search · <em>hybrid · tiered · fallback</em>",
                "Search by meaning: combine inverted index (Elastic) with semantic index (embeddings). Hands-on RAG learning project.",
                ["question", "keyword ± meaning", "rerank", "top-k"],
            ),
            cards_slide(
                "Why",
                "hybrid",
                "Keywords alone miss synonyms",
                [
                    ("kw", "BM25 / Elastic", "Fast and cheap — but “car” ≠ “automobile”."),
                    ("sem", "Embeddings", "Catch meaning — heavier per query."),
                    ("both", "Combine", "Filter by keyword, rank by meaning."),
                ],
                "02",
                "notes/semantic-search.md",
            ),
            ideas_slide(
                "Strategies",
                "notes/semantic-search.md",
                [
                    ("hyb", "Hybrid", "Keyword filters candidates; semantic reranks."),
                    ("tier", "Tiered", "Easy → keyword; hard → semantic (complexity router)."),
                    ("fall", "Fallback", "Semantic first; fall back to keyword if weak."),
                ],
                "03",
                "hybrid · tiered · fallback · MS MARCO",
            ),
            img_slide("semantic-hybrid.svg", "../assets/semantic-hybrid.svg", "Two indexes", "04"),
            img_slide("search-twoway.svg", "../assets/search-twoway.svg", "Two-way search", "05"),
            img_slide("embed-then-query.jpg", "../../notes/assets/protonx/embed-then-query.jpg", "Retrieve step", "06"),
            img_slide("rag-advanced.jpg", "../../notes/assets/protonx/rag-advanced.jpg", "Advanced retrieve", "07"),
            table_slide(
                "Indexes",
                "compare",
                "Two index types",
                ["Index", "Strong", "Weak"],
                [
                    ["Inverted (Elastic)", "Fast, exact terms", "No synonym understanding"],
                    ["Semantic (vectors)", "Meaning / paraphrase", "Heavier; needs a model"],
                ],
                "08",
                "notes/semantic-search.md",
            ),
            cards_slide(
                "Eval",
                "MS MARCO",
                "How to know it works",
                [
                    ("data", "MS MARCO", "Real questions + relevant passages."),
                    ("mrr", "MRR@10 / P@k", "Rank quality metrics."),
                    ("clf", "Query classifier", "Labels easy vs hard for Tiered."),
                ],
                "09",
                "github.com/hoanganh25991/semantic-search",
            ),
            pipeline_slide(
                "Pipeline",
                "Question to top-k",
                ["question", "classify?", "keyword|semantic", "merge", "top-k", "RAG"],
                "10",
                "stands on embedding + vector-db",
            ),
            close_slide(
                "Open the repo<br /><em>and the note.</em>",
                "notes/semantic-search.md · github.com/hoanganh25991/semantic-search",
                "../../notes/semantic-search.html",
                "Open note →",
            ),
        ]
    )
    return SHELL.format(title="Semantic search · slides", body=body)


def deck_skills_rules() -> str:
    body = "".join(
        [
            title_slide(
                "Concept · skills-rules",
                "teaching",
                "Skills · Rules · <em>Commands</em>",
                "Three ways to teach a coding agent: packaged capability, always-on constraint, and typed shortcuts.",
                ["Skill", "Rule", "Command", "~/.agents"],
            ),
            cards_slide(
                "Why",
                "matters",
                "Same model, better brain config",
                [
                    ("proc", "Process once", "Stop repeating instructions every turn."),
                    ("conv", "Conventions stick", "Rules enforce project style automatically."),
                    ("trig", "Auto-trigger", "Skill descriptions tell the agent when to load."),
                ],
                "02",
                "notes/skills-rules.md",
            ),
            ideas_slide(
                "Three layers",
                "notes/skills-rules.md",
                [
                    ("skill", "Skill", "SKILL.md (+ scripts) loaded when the task matches."),
                    ("rule", "Rule", "Always-on or glob-matched constraint."),
                    ("cmd", "Command", "User types /deep-plan, /loop, /graphify."),
                ],
                "03",
                "skills · rules · commands · ~/.agents",
            ),
            img_slide("skills-rules-commands.png", "../assets/skills-rules-commands.png", "Three concepts", "04"),
            img_slide("skills-layers.svg", "../assets/skills-layers.svg", "Layers", "05"),
            table_slide(
                "Compare",
                "when",
                "When each layer loads",
                ["Kind", "When", "Example"],
                [
                    ["Skill", "Task matches description", "frontend-slides · tavily-*"],
                    ["Rule", "Always or file glob", "commit style · notes-first"],
                    ["Command", "User types shortcut", "/deep-plan · /graphify ."],
                ],
                "06",
                "notes/skills-rules.md",
            ),
            cards_slide(
                "SKILL.md",
                "structure",
                "Description is the trigger",
                [
                    ("home", "~/.agents/skills", "Canonical path — write once, use everywhere."),
                    ("desc", "description field", "“Use when…” — the model auto-picks from this."),
                    ("scripts", "Scripts OK", "Agent runs helpers via shell / MCP."),
                ],
                "07",
                "notes/skills-rules.md",
            ),
            cards_slide(
                "Rules",
                "budget",
                "Keep always-rules short",
                [
                    ("ctx", "Context cost", "Always rules burn tokens every turn."),
                    ("glob", "Prefer globs", "*.tsx / notes/*.md load only when relevant."),
                    ("split", "Rules vs skills", "Conventions in rules; processes in skills."),
                ],
                "08",
                "notes/skills-rules.md",
            ),
            cards_slide(
                "Clients",
                "layout",
                "Global home layout",
                [
                    ("src", "~/.agents/skills", "Source of truth"),
                    ("empty", "Cursor/Claude skills dirs", "Keep empty — don't duplicate trees"),
                    ("pi", "Pi", "Symlinks → ~/.agents only"),
                ],
                "09",
                "related: mcp · agents",
            ),
            close_slide(
                "Configure the brain,<br /><em>then call tools.</em>",
                "notes/skills-rules.md · try demos/mcp app",
                "../../demos/mcp/app/index.html",
                "Open MCP demo →",
            ),
        ]
    )
    return SHELL.format(title="Skills · Rules · Commands · slides", body=body)


def deck_train_gpu() -> str:
    body = "".join(
        [
            title_slide(
                "Concept · train-gpu",
                "teaching",
                "Train · <em>PyTorch / TF · GPU</em>",
                "Where models actually learn: HF/Kaggle data, PyTorch or TensorFlow, many GPU epochs, then export weights.",
                ["data", "notebook", "GPU epochs", "checkpoint", "demo"],
            ),
            cards_slide(
                "Why",
                "checklist",
                "Demos are inference — training is elsewhere",
                [
                    ("lab", "Browser demos", "Show the flow; they do not replace GPU training."),
                    ("real", "Real learning", "Needs labeled data + GPU hours."),
                    ("plug", "Then plug in", "Export checkpoint → embed in UI demos."),
                ],
                "02",
                "notes/train-gpu.md",
            ),
            ideas_slide(
                "Stack",
                "notes/train-gpu.md",
                [
                    ("pt", "PyTorch", "Flexible loop — most lab training code."),
                    ("tf", "TensorFlow", "Softmax regression + Embedding Projector."),
                    ("data", "HF + Kaggle", "Pre-labeled data ready to download."),
                ],
                "03",
                "pytorch · tensorflow · GPU · huggingface · kaggle",
            ),
            img_slide("train-gpu-stack.png", "../assets/train-gpu-stack.png", "GPU stack", "04"),
            table_slide(
                "Layers",
                "two",
                "Training vs inference",
                ["Layer", "Job", "Output"],
                [
                    ["Training", "HF/Kaggle → GPU epochs", "checkpoint"],
                    ["Inference", "load model → predict", "label / action"],
                ],
                "05",
                "see train-infer.md",
            ),
            pipeline_slide(
                "Workflow",
                "Short practical path",
                ["pick dataset", "write notebook", "GPU train", "watch metrics", "export", "demo"],
                "06",
                "notes/train-gpu.md",
            ),
            cards_slide(
                "Runtime",
                "where",
                "Where to run epochs",
                [
                    ("colab", "Google Colab", "Quick GPU notebooks in the browser."),
                    ("kaggle", "Kaggle", "Free GPU/TPU with datasets attached."),
                    ("cloud", "Cloud endpoint", "When you need sustained training."),
                ],
                "07",
                "notes/train-gpu.md",
            ),
            cards_slide(
                "Watch",
                "metrics",
                "Train until good enough",
                [
                    ("loss", "Loss / accuracy", "Watch train and val together."),
                    ("stop", "~95%+", "Good enough for many demos — then export."),
                    ("infer", "Back to UI", "car-nn · sentiment · softmax demos."),
                ],
                "08",
                "demos",
            ),
            cards_slide(
                "Related",
                "notes",
                "Deep links",
                [
                    ("pt", "pytorch-training", "Manual loop details."),
                    ("tf", "tensorflow-training", "compile + fit."),
                    ("ti", "train-infer", "Mental model of two phases."),
                ],
                "09",
                "related",
            ),
            close_slide(
                "Train on GPU,<br /><em>infer in the lab.</em>",
                "notes/train-gpu.md",
                "../../notes/train-gpu.html",
                "Open note →",
            ),
        ]
    )
    return SHELL.format(title="Train GPU · slides", body=body)


def deck_train_infer() -> str:
    body = "".join(
        [
            title_slide(
                "Concept · train-infer",
                "teaching",
                "Train → <em>Inference</em>",
                "Every model lives two lives: learn weights once (heavy), then predict lightly many times.",
                ["data", "train", "checkpoint", "infer"],
            ),
            cards_slide(
                "Why",
                "split",
                "Stop treating “AI” as one block",
                [
                    ("once", "Train once", "Many GPU epochs → checkpoint file."),
                    ("many", "Infer many", "Every user click loads weights and predicts."),
                    ("lab", "Lab demos", "All inference — training happened in notebooks."),
                ],
                "02",
                "notes/06-train-infer.md",
            ),
            ideas_slide(
                "Two phases",
                "notes/06-train-infer.md",
                [
                    ("train", "Train", "Loop data, measure loss, update weights."),
                    ("ckpt", "Checkpoint", "The product — inference needs no training data."),
                    ("infer", "Inference", "Load weights → feed input → label/action."),
                ],
                "03",
                "train · inference · checkpoint",
            ),
            img_slide("train-infer-split.png", "../assets/train-infer-split.png", "Train vs infer", "04"),
            img_slide("train-infer-flow.svg", "../assets/train-infer-flow.svg", "Two lives", "05"),
            table_slide(
                "Compare",
                "cost",
                "Cost and output",
                ["Phase", "Cost", "Output"],
                [
                    ["Train", "Heavy · needs GPU", "checkpoint (weights)"],
                    ["Inference", "Light · realtime", "label / action"],
                ],
                "06",
                "notes/06-train-infer.md",
            ),
            cards_slide(
                "Learning",
                "loss",
                "Learning = reducing error",
                [
                    ("pred", "Predict", "Model outputs scores / probs."),
                    ("loss", "Measure", "Cross-entropy with softmax for classifiers."),
                    ("nudge", "Update", "Nudge weights toward lower loss."),
                ],
                "07",
                "notes/softmax.md",
            ),
            pipeline_slide(
                "Pipeline",
                "End to end",
                ["data", "train (GPU)", "checkpoint", "load", "infer"],
                "08",
                "notes/06-train-infer.md",
            ),
            cards_slide(
                "In the lab",
                "practice",
                "Where each half lives",
                [
                    ("nb", "Notebooks", "protonx / Kaggle / Colab — real training."),
                    ("ui", "Browser demos", "car-nn · sentiment — inference only."),
                    ("stack", "train-gpu.md", "Full tool checklist."),
                ],
                "09",
                "related",
            ),
            close_slide(
                "Learn once,<br /><em>predict forever.</em>",
                "notes/06-train-infer.md",
                "../../notes/train-infer.html",
                "Open note →",
            ),
        ]
    )
    return SHELL.format(title="Train → Inference · slides", body=body)


def deck_agents() -> str:
    body = "".join(
        [
            title_slide(
                "Concept · agents",
                "teaching",
                "AI Agents · <em>harness comparison</em>",
                "Harness ≠ model. Orchestration software (UI, tools, context, loop) shapes how the same brain feels.",
                ["model", "harness", "tools", "loop"],
            ),
            cards_slide(
                "Why",
                "matters",
                "Half the story is the harness",
                [
                    ("ctx", "Context", "Which files get into the prompt."),
                    ("tools", "Tool calling", "MCP, shell, browser — smoothness differs."),
                    ("loop", "Agent loop", "Self-correct, test, ask back."),
                ],
                "02",
                "notes/07-agents.md",
            ),
            ideas_slide(
                "Harness",
                "notes/07-agents.md",
                [
                    ("def", "Harness", "UI + tools + context + agent loop."),
                    ("model", "Model", "The brain plugged in — compare in model-notes."),
                    ("feel", "Same model, different feel", "Cursor vs Claude Code can feel opposite."),
                ],
                "03",
                "agents · harness · cursor · claude · pi",
            ),
            img_slide("agents-harness.png", "../assets/agents-harness.png", "Harnesses", "04"),
            table_slide(
                "Compare",
                "field notes",
                "Personal harness notes",
                ["Harness", "Strength", "Feel"],
                [
                    ["Cursor", "Fast feedback · MCP · skills", "Fastest loop"],
                    ["Claude Code", "Clarify context · hard skills", "Solid, slower"],
                    ["Pi", "Global ~/.agents · light", "Minimal overhead"],
                    ["Cline / Kilo", "Open · customizable", "Self-directed tests"],
                    ["OpenCode", "Many models via OpenRouter", "Open source"],
                    ["Zed", "Fast editor", "Lighter agent"],
                ],
                "05",
                "notes/07-agents.md",
            ),
            cards_slide(
                "Cursor",
                "auto",
                "Auto vs fixed model",
                [
                    ("auto", "Auto", "Fast routing — quality can vary."),
                    ("fixed", "Fixed (e.g. Grok 4.5)", "Controllable; often better than Auto in practice."),
                    ("budget", "Token efficiency", "Worth watching — quality per dollar."),
                ],
                "06",
                "notes/08-model-notes.md",
            ),
            cards_slide(
                "Differs",
                "axes",
                "What harnesses differ on",
                [
                    ("ctx", "Context management", "Compress / select files for the prompt."),
                    ("mcp", "Tool calling", "MCP + shell reliability."),
                    ("skills", "Skills / rules", "Loading ~/.agents know-how."),
                ],
                "07",
                "notes/skills-rules.md",
            ),
            cards_slide(
                "First mate",
                "crew",
                "Orchestrating crewmates",
                [
                    ("role", "First mate", "Agent that knows what to do and coordinates."),
                    ("agents", "agents.md", "Declare instructions for the crew."),
                    ("lab", "Lab links", "MCP demo · complexity router."),
                ],
                "08",
                "demos",
            ),
            cards_slide(
                "Homes",
                "paths",
                "Where know-how lives",
                [
                    ("skills", "~/.agents/skills", "Global skills"),
                    ("setup", "agents-setup", "Skill trials"),
                    ("graph", "graphify", "Codebase link viz"),
                ],
                "09",
                "related",
            ),
            close_slide(
                "Pick a harness,<br /><em>then a model.</em>",
                "notes/07-agents.md · try demos/mcp",
                "../../demos/mcp/app/index.html",
                "Open MCP demo →",
            ),
        ]
    )
    return SHELL.format(title="AI Agents · slides", body=body)


def deck_model_notes() -> str:
    body = "".join(
        [
            title_slide(
                "Field notes · model-notes",
                "teaching",
                "Model field notes · <em>≠ harness</em>",
                "Notes on the models themselves (OpenRouter + Cursor). Harness comparison lives in agents.",
                ["pick model", "task fit", "cost", "speed"],
            ),
            cards_slide(
                "Why",
                "split",
                "Harness shapes workflow — model shapes reasoning",
                [
                    ("qual", "Quality", "Reasoning depth and reliability."),
                    ("spd", "Speed", "Tokens per second / latency."),
                    ("$", "Cost", "Intelligence per dollar and per minute."),
                ],
                "02",
                "notes/08-model-notes.md",
            ),
            img_slide("model-notes-spectrum.png", "../assets/model-notes-spectrum.png", "Spectrum", "03"),
            table_slide(
                "Field",
                "table",
                "Personal experience (not benchmarks)",
                ["Model", "Strong", "Watch"],
                [
                    ["Grok 4.5", "Fast · smooth · good $/task", "Hallucination on unverifiable"],
                    ["Composer Fast", "Very fast replies", "Costs more than Auto"],
                    ["Cursor Auto", "Fast feedback loop", "Quality varies with routing"],
                    ["Anthropic", "Clarify · skills · ask back", "Slow · session limits"],
                    ["DeepSeek V4", "Debug existing code", "No images · weaker greenfield"],
                    ["Qwen 3", "Simple tasks", "Weak on large greenfield"],
                ],
                "04",
                "notes/08-model-notes.md",
            ),
            cards_slide(
                "Grok 4.5",
                "why",
                "Why it impresses (mid-2026)",
                [
                    ("tps", "~80 TPS", "Optimized for coding + agentic work."),
                    ("tok", "Fewer tokens", "~4.2× fewer output tokens vs Opus on SWE-Bench Pro."),
                    ("edge", "Intel / time / $", "Wins on verifiable coding tasks."),
                ],
                "05",
                "notes/08-model-notes.md",
            ),
            cards_slide(
                "Principles",
                "pick",
                "Match model to job",
                [
                    ("new", "Greenfield", "Favor strong reasoning (Anthropic, Grok)."),
                    ("fix", "Debug existing", "DeepSeek V4 — effective and cheap."),
                    ("img", "Needs images", "Avoid DeepSeek (no image input)."),
                ],
                "06",
                "notes/08-model-notes.md",
            ),
            cards_slide(
                "More",
                "rules of thumb",
                "Speed · clarify · budget",
                [
                    ("fast", "Speed + low cost", "Grok 4.5 / Composer Fast."),
                    ("ask", "Clarify constraints", "Anthropic strongest at asking back."),
                    ("bench", "Check boards", "OpenRouter prices · LMArena votes."),
                ],
                "07",
                "references",
            ),
            cards_slide(
                "Related",
                "links",
                "Keep the split clean",
                [
                    ("harness", "07-agents.md", "Compare Cursor / Claude Code / Pi…"),
                    ("skills", "skills-rules.md", "Configure know-how."),
                    ("mcp", "mcp.md", "Tools the harness can call."),
                ],
                "08",
                "related",
            ),
            close_slide(
                "Model for the task,<br /><em>harness for the loop.</em>",
                "notes/08-model-notes.md",
                "../../notes/model-notes.html",
                "Open note →",
            ),
        ]
    )
    return SHELL.format(title="Model field notes · slides", body=body)


def deck_ai_timeline() -> str:
    body = "".join(
        [
            title_slide(
                "Field notes · ai-timeline",
                "teaching",
                "AI timeline · <em>my journey</em>",
                "2023 → present: from first LLM exposure through RAG to agents and automation — anchored to real milestones.",
                ["2023 basics", "2024 agents", "MCP", "2026 automation"],
            ),
            cards_slide(
                "Why",
                "map",
                "Order explains the lab",
                [
                    ("path", "My path", "Fundamentals → RAG → agents."),
                    ("hinge", "MCP hinge", "Nov 2024 — tools for agents."),
                    ("keep", "Old notes still matter", "Tokenize / attention / RAG underpin every agent."),
                ],
                "02",
                "notes/10-ai-timeline.md",
            ),
            img_slide("ai-timeline-hero.png", "../assets/ai-timeline-hero.png", "Timeline hero", "03"),
            img_slide("ai-timeline-strip.svg", "../assets/ai-timeline-strip.svg", "Strip", "04"),
            cards_slide(
                "2023",
                "stage 1",
                "First LLM exposure + foundations",
                [
                    ("start", "ChatGPT wave", "Late 2022 → serious learning in 2023."),
                    ("mar", "Mar 2023", "GPT-4 · Claude 1 · Llama 1 · RAG boom."),
                    ("order", "Learn order", "tokenize → embedding → attention → softmax → RAG."),
                ],
                "05",
                "notes/10-ai-timeline.md",
            ),
            cards_slide(
                "2024",
                "stage 2",
                "Stronger models + coding agents",
                [
                    ("ctx", "Long context", "Gemini 1.5 · 1M context."),
                    ("code", "Coding jump", "Claude 3.5 Sonnet · Cursor takes off."),
                    ("shift", "From reading to building", "Use AI to code for real."),
                ],
                "06",
                "notes/10-ai-timeline.md",
            ),
            cards_slide(
                "2024–25",
                "stage 3",
                "Agent era — MCP · skills · harness",
                [
                    ("mcp", "Nov 25, 2024", "MCP launches — hinge event."),
                    ("harness", "2025", "Claude Code · AGENTS.md · skills/rules."),
                    ("lab", "Lab pivot", "mcp · skills-rules · agents notes."),
                ],
                "07",
                "notes/mcp.md",
            ),
            cards_slide(
                "2026",
                "stage 4",
                "Model wave + automation (now)",
                [
                    ("models", "Model wave", "Opus 4.8 · Fable 5 · Grok 4.5 · GPT-5.6."),
                    ("auto", "Automation", "OpenClaw (pi) → Hermess polish."),
                    ("focus", "Focus now", "model-notes · agent-automation."),
                ],
                "08",
                "notes/09-agent-automation.md",
            ),
            table_slide(
                "Milestones",
                "table",
                "Anchors in the lab",
                ["When", "Event", "In the lab"],
                [
                    ["2023", "First LLM exposure", "tokenize · embed · attn · softmax · RAG"],
                    ["2024", "Coding agents", "using AI to build"],
                    ["Nov 2024", "MCP", "mcp note + demo"],
                    ["2025", "Harness · skills", "agents · skills-rules"],
                    ["2026", "Grok 4.5 · automation", "model-notes · Hermess"],
                ],
                "09",
                "notes/10-ai-timeline.md",
            ),
            cards_slide(
                "Takeaways",
                "now",
                "Understanding → steering",
                [
                    ("arc", "Arc", "Understand models (2023–24) → steer agents (late 2024+)."),
                    ("hinge", "Hinge", "MCP — agent ↔ tool standard."),
                    ("watch", "Watch", "Harnesses · model waves · automation."),
                ],
                "10",
                "related",
            ),
            close_slide(
                "Concepts still hold;<br /><em>agents steer them.</em>",
                "notes/10-ai-timeline.md",
                "../../notes/ai-timeline.html",
                "Open note →",
            ),
        ]
    )
    return SHELL.format(title="AI timeline · slides", body=body)


DECKS = {
    "classification": deck_classification,
    "pytorch-training": deck_pytorch,
    "tensorflow-training": deck_tensorflow,
    "huggingface": deck_huggingface,
    "kaggle": deck_kaggle,
    "transformer": deck_transformer,
    "sentence-transformers": deck_sentence_transformers,
    "vector-database": deck_vector_database,
    "semantic-search": deck_semantic_search,
    "skills-rules": deck_skills_rules,
    "train-gpu": deck_train_gpu,
    "train-infer": deck_train_infer,
    "agents": deck_agents,
    "model-notes": deck_model_notes,
    "ai-timeline": deck_ai_timeline,
}


def main() -> None:
    write_svgs()
    for slug, fn in DECKS.items():
        out = SLIDES / slug / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        html = fn()
        # ensure first slide has active
        if 'class="slide active"' not in html:
            html = html.replace('class="slide"', 'class="slide active"', 1)
        out.write_text(html, encoding="utf-8")
        n = html.count('class="slide')
        print(f"  wrote {out.relative_to(ROOT)} ({n} slides)")
    print(f"done · {len(DECKS)} decks + SVGs")


if __name__ == "__main__":
    main()
