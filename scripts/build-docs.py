#!/usr/bin/env python3
"""Build the AI Lab docs site.

Source of truth (3 siblings):
    notes/*.md + notes/catalog.json   knowledge (primary)
    slides/<topic>/index.html         presentation decks
    demos/<topic>/app/index.html      interactive apps

Output (the only place you open / serve):
    docs/index.html                   search-first hub, list view
    docs/notes/<id>.html              full document page per note
    docs/slides/**  docs/demos/**     copied decks / apps
    docs/search-index.json            client search payload

Re-run after editing notes/, catalog.json, slides/, or demos/:

    python3 scripts/build-docs.py
"""

from __future__ import annotations

import json
import posixpath
import re
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "notes" / "catalog.json"
DOCS = ROOT / "docs"
NOTES_OUT = DOCS / "notes"

# Virtual repo root so we can resolve/rewrite relative links deterministically.
VROOT = "/R"


# --------------------------------------------------------------------------- #
# Markdown → HTML (no deps)                                                    #
# --------------------------------------------------------------------------- #
def strip_md(text: str) -> str:
    text = re.sub(r"```[\s\S]*?```", " ", text)
    text = re.sub(r"`[^`]+`", " ", text)
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1 ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1 ", text)
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.M)
    text = re.sub(r"[>*_|#-]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def inline(s: str) -> str:
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    return s


def md_to_html(md: str) -> str:
    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    in_code = False
    in_ul = False
    in_table = False

    def close_ul() -> None:
        nonlocal in_ul
        if in_ul:
            out.append("</ul>")
            in_ul = False

    def close_table() -> None:
        nonlocal in_table
        if in_table:
            out.append("</tbody></table>")
            in_table = False

    for line in lines:
        if line.strip().startswith("```"):
            close_ul()
            close_table()
            if not in_code:
                out.append("<pre><code>")
                in_code = True
            else:
                out.append("</code></pre>")
                in_code = False
            continue
        if in_code:
            out.append(
                line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") + "\n"
            )
            continue

        if re.match(r"^\|", line) and "|" in line[1:]:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(re.match(r"^:?-+:?$", c.replace(" ", "")) for c in cells):
                continue
            if not in_table:
                close_ul()
                out.append("<table><tbody>")
                in_table = True
                out.append("<tr>" + "".join(f"<th>{inline(c)}</th>" for c in cells) + "</tr>")
            else:
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>")
            continue
        else:
            close_table()

        m = re.match(r"^(#{1,3})\s+(.*)$", line)
        if m:
            close_ul()
            level = len(m.group(1))
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            continue

        if re.match(r"^[-*]\s+", line):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            item = re.sub(r"^[-*]\s+", "", line)
            out.append(f"<li>{inline(item)}</li>")
            continue
        else:
            close_ul()

        if not line.strip():
            continue
        if line.strip().startswith(">"):
            out.append(f"<blockquote>{inline(line.strip().lstrip('> ').strip())}</blockquote>")
            continue
        out.append(f"<p>{inline(line)}</p>")

    close_ul()
    close_table()
    if in_code:
        out.append("</code></pre>")
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# Link rewriting                                                               #
# --------------------------------------------------------------------------- #
def _resolve(base_vdir: str, href: str) -> str:
    """Resolve a relative href against a virtual base dir → normalized vpath."""
    return posixpath.normpath(posixpath.join(base_vdir, href))


def _remap_copied(vpath: str) -> str:
    """demos/ and slides/ are copied under docs/ — point links at the copies."""
    for prefix in ("/R/demos/", "/R/slides/"):
        if vpath.startswith(prefix):
            return "/R/docs" + vpath[len("/R"):]
    return vpath


def rewrite_href(href: str, base_vdir: str, out_vdir: str, file2id: dict[str, str]) -> str:
    """Rewrite one href from `base_vdir` context to be correct from `out_vdir`."""
    if not href or re.match(r"^[a-z]+:", href) or href.startswith("#"):
        return href
    vpath = _resolve(base_vdir, href)

    # note .md → generated sibling page
    if vpath.startswith("/R/notes/") and vpath.endswith(".md"):
        base = posixpath.basename(vpath)
        nid = file2id.get(base)
        if nid:
            vpath = f"/R/docs/notes/{nid}.html"
        # else keep pointing at raw source .md (below)

    vpath = _remap_copied(vpath)
    return posixpath.relpath(vpath, out_vdir)


def rewrite_html_links(html: str, base_vdir: str, out_vdir: str, file2id: dict[str, str]) -> str:
    def sub(m: re.Match) -> str:
        return 'href="' + rewrite_href(m.group(1), base_vdir, out_vdir, file2id) + '"'

    return re.sub(r'href="([^"]+)"', sub, html)


# --------------------------------------------------------------------------- #
# Payload                                                                      #
# --------------------------------------------------------------------------- #
def build_payload() -> tuple[dict, list[dict]]:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    entries = catalog["notes"]
    file2id = {posixpath.basename(e["file"]): e["id"] for e in entries}

    search_notes: list[dict] = []
    page_notes: list[dict] = []

    for entry in entries:
        path = ROOT / entry["file"]
        raw = path.read_bytes().decode("utf-8", errors="replace") if path.is_file() else ""

        body_html = md_to_html(raw) if raw else "<p>(missing source)</p>"
        # note pages live in docs/notes → rewrite internal links from that context
        body_html = rewrite_html_links(body_html, "/R/notes", "/R/docs/notes", file2id)

        body_text = strip_md(raw)
        search_text = strip_md(
            " ".join(
                [
                    entry.get("title") or "",
                    entry.get("summary") or "",
                    " ".join(entry.get("topics") or []),
                    raw,
                ]
            )
        ).lower()

        # hub links (context: docs/index.html at /R/docs)
        slides = entry.get("slides")
        demo = entry.get("demo")
        extra = []
        for l in entry.get("extra_links") or []:
            extra.append(
                {
                    "label": l["label"],
                    "href": rewrite_href(l["href"], VROOT, "/R/docs", file2id),
                }
            )

        search_notes.append(
            {
                "id": entry["id"],
                "title": entry["title"],
                "summary": entry.get("summary") or "",
                "topics": entry.get("topics") or [],
                "group": entry.get("group") or "concept",
                "page": f"notes/{entry['id']}.html",
                "slides": rewrite_href(slides, VROOT, "/R/docs", file2id) if slides else None,
                "demo": rewrite_href(demo, VROOT, "/R/docs", file2id) if demo else None,
                "extra_links": extra,
                "search_text": search_text,
                "body_text": body_text,
            }
        )

        page_notes.append(
            {
                "id": entry["id"],
                "title": entry["title"],
                "summary": entry.get("summary") or "",
                "topics": entry.get("topics") or [],
                "group": entry.get("group") or "concept",
                "body_html": body_html,
                # note-page links (context: docs/notes)
                "slides": rewrite_href(slides, VROOT, "/R/docs/notes", file2id) if slides else None,
                "demo": rewrite_href(demo, VROOT, "/R/docs/notes", file2id) if demo else None,
                # raw.md is copied next to the note page for Download
                "raw": posixpath.basename(entry["file"]),
                "raw_src": entry["file"],
                "extra_links": [
                    {
                        "label": l["label"],
                        "href": rewrite_href(l["href"], VROOT, "/R/docs/notes", file2id),
                    }
                    for l in (entry.get("extra_links") or [])
                ],
            }
        )

    payload = {
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "synonyms": SYNONYMS,
        "notes": search_notes,
    }
    return payload, page_notes


# Bidirectional synonym groups (folded, lowercase). Every word in a group
# expands to the others at query time.
SYNONYMS = [
    ["tokenize", "tokenizer", "token", "bpe", "wordpiece", "subword", "vocabulary"],
    ["embedding", "embed", "vector", "cosine", "cbow", "similarity"],
    ["attention", "qkv", "transformer", "self-attention"],
    ["softmax", "logits", "probability", "classifier", "classification"],
    ["rag", "retrieve", "retrieval", "vector-db", "chunks", "grounded"],
    ["mcp", "tool", "tools", "protocol", "server"],
    ["skill", "skills", "rule", "rules", "command", "commands", "agents-md"],
    ["agent", "agents", "harness", "cursor", "claude", "pi", "cline", "opencode", "zed"],
    ["automation", "openclaw", "hermess", "pi", "orchestrate", "agentic"],
    ["model", "models", "openrouter", "llm", "grok", "deepseek", "qwen", "kimi", "glm", "composer"],
    ["train", "training", "epoch", "gpu", "pytorch", "tensorflow", "inference", "checkpoint"],
    ["search", "find", "query", "follow-up"],
    ["kb", "knowledge-base", "personal-kb", "personal-knowledge-base", "taxonomy", "youtube", "graph-rag", "first-mate"],
    ["timeline", "history", "milestone", "era", "transformer", "bert"],
]


# --------------------------------------------------------------------------- #
# Shared light theme                                                           #
# --------------------------------------------------------------------------- #
THEME_CSS = r"""
:root {
  --bg: #eef3f9; --surface: #ffffff; --ink: #16202e; --muted: #5a6b80;
  --teal: #0f8a9b; --teal-soft: rgba(15,138,155,.12); --amber: #c2703a;
  --line: rgba(20,32,46,.12); --line-soft: rgba(20,32,46,.07);
  --shadow: 0 1px 2px rgba(20,32,46,.05), 0 8px 24px rgba(20,32,46,.06);
  --font: Sora, system-ui, sans-serif; --serif: "Instrument Serif", Georgia, serif;
  --mono: "IBM Plex Mono", ui-monospace, monospace;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  min-height: 100vh; color: var(--ink); font-family: var(--font);
  background:
    radial-gradient(ellipse 60% 45% at 88% -5%, rgba(15,138,155,.10), transparent 60%),
    radial-gradient(ellipse 55% 45% at 0% 105%, rgba(194,112,58,.08), transparent 55%),
    var(--bg);
  -webkit-font-smoothing: antialiased;
}
a { color: var(--teal); }
::selection { background: var(--teal-soft); }
"""


# --------------------------------------------------------------------------- #
# Hub template                                                                 #
# --------------------------------------------------------------------------- #
HUB_HTML = r"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>AI Lab</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&family=Sora:wght@400;500;600;700&display=swap" rel="stylesheet" />
<style>
@@THEME@@
.shell { max-width: 880px; margin: 0 auto; padding: 56px 22px 96px; }
.brand {
  display: block; text-decoration: none; color: inherit;
  line-height: 0;
}
.brand img {
  display: block; height: 64px; width: auto; max-width: min(420px, 100%);
  object-fit: contain; object-position: left center;
}
.tagline { margin-top: 14px; color: var(--muted); font-size: 15px; max-width: 560px; line-height: 1.5; }
.search-wrap { position: relative; margin: 30px 0 10px; }
#q {
  width: 100%; background: var(--surface); border: 1px solid var(--line);
  border-radius: 14px; padding: 18px 20px 18px 52px; color: var(--ink);
  font: 500 18px var(--font); box-shadow: var(--shadow);
}
#q:focus { outline: none; border-color: var(--teal); box-shadow: 0 0 0 4px var(--teal-soft); }
.search-wrap svg { position: absolute; left: 20px; top: 50%; transform: translateY(-50%); color: var(--muted); }
.meta-line { font-family: var(--mono); font-size: 12px; color: var(--muted); margin: 10px 2px 22px; }
.filters { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 26px; }
.filters button {
  background: var(--surface); border: 1px solid var(--line); color: var(--muted);
  border-radius: 999px; padding: 8px 14px; font: 500 12px var(--mono); cursor: pointer;
  transition: all .15s;
}
.filters button:hover { border-color: var(--teal); color: var(--teal); }
.filters button.on { background: var(--teal); border-color: var(--teal); color: #fff; }
.section-label {
  font: 500 11px var(--mono); letter-spacing: .16em; text-transform: uppercase;
  color: var(--muted); margin: 26px 2px 12px;
}
.list { display: flex; flex-direction: column; gap: 8px; }
.row {
  display: block; text-decoration: none; color: inherit; background: var(--surface);
  border: 1px solid var(--line); border-radius: 14px; padding: 16px 18px;
  transition: border-color .15s, transform .15s, box-shadow .15s;
}
.row:hover { border-color: var(--teal); transform: translateY(-1px); box-shadow: var(--shadow); }
.row-top { display: flex; align-items: baseline; gap: 10px; flex-wrap: wrap; }
.row h3 { font-size: 17px; font-weight: 600; letter-spacing: -.01em; }
.row .grp { font: 500 10px var(--mono); letter-spacing: .1em; text-transform: uppercase; color: var(--muted); }
.row .badge {
  font: 500 10px var(--mono); letter-spacing: .05em; text-transform: uppercase;
  padding: 3px 8px; border-radius: 999px; border: 1px solid var(--line-soft); color: var(--muted);
}
.row .badge.on { color: var(--teal); border-color: var(--teal-soft); background: var(--teal-soft); }
.row p { color: var(--muted); font-size: 13.5px; line-height: 1.5; margin: 7px 0 0; }
.row .snippet { font-size: 13px; margin-top: 8px; color: var(--ink); opacity: .82; }
.row .topics { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px; }
.row .topics span { font: 500 11px var(--mono); color: var(--amber); }
.spacer { flex: 1; }
.badges { display: flex; gap: 6px; }
mark { background: rgba(194,112,58,.22); color: inherit; border-radius: 3px; padding: 0 2px; }
.followup {
  background: var(--surface); border: 1px dashed var(--line); border-radius: 14px;
  padding: 18px 20px; margin-top: 6px;
}
.followup h4 { font-size: 14px; margin-bottom: 6px; }
.followup p { color: var(--muted); font-size: 13px; line-height: 1.5; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
.chips button {
  background: var(--teal-soft); border: 1px solid var(--teal-soft); color: var(--teal);
  border-radius: 999px; padding: 7px 13px; font: 500 12px var(--mono); cursor: pointer;
}
.chips button:hover { border-color: var(--teal); }
.empty { color: var(--muted); font-size: 14px; }
footer { margin-top: 40px; font: 12px var(--mono); color: var(--muted); }
</style>
</head>
<body>
<div class="shell">
  <a class="brand" href="./index.html" aria-label="AI Lab">
    <img src="notes/assets/ai-lab-logo.png" alt="AI Lab" width="420" height="120" />
  </a>
  <p class="tagline">Notes are the source of truth. Search first — mở note dạng document, slides &amp; demo hiện khi có.</p>

  <form class="search-wrap" id="searchForm" autocomplete="off">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
    <input id="q" type="search" placeholder="Tìm: tokenize, rag, mcp, skills, grok…" />
  </form>
  <p class="meta-line" id="metaLine">Loading…</p>

  <div id="results"></div>

  <footer id="foot"></footer>
</div>

<script id="NOTES_DATA" type="application/json">@@NOTES_JSON@@</script>
<script>
(function () {
  const payload = JSON.parse(document.getElementById("NOTES_DATA").textContent);
  const notes = payload.notes || [];
  const synGroups = payload.synonyms || [];
  let query = "";

  // ---- text utils -------------------------------------------------------- //
  function fold(s) {
    return String(s || "")
      .toLowerCase()
      .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
      .replace(/đ/g, "d");
  }
  // synonym lookup: word -> Set(all words in its groups)
  const synMap = {};
  for (const g of synGroups) {
    for (const w of g) {
      const k = fold(w);
      (synMap[k] || (synMap[k] = new Set())).add(k);
      for (const w2 of g) synMap[k].add(fold(w2));
    }
  }
  function expand(tok) {
    const out = new Set([tok]);
    if (synMap[tok]) synMap[tok].forEach((x) => out.add(x));
    return [...out];
  }
  function tokenize(q) {
    return fold(q).split(/[^a-z0-9_+.-]+/i).filter((t) => t.length > 1);
  }

  function escapeHtml(s) {
    return String(s ?? "").replace(/[&<>"']/g, (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  // ---- scoring ----------------------------------------------------------- //
  function scoreNote(n, toks) {
    if (!toks.length) return { s: 1, hit: null };
    const title = fold(n.title);
    const summary = fold(n.summary);
    const topics = (n.topics || []).map(fold);
    const body = fold(n.search_text || "");
    let s = 0;
    let matchedAll = true;
    for (const raw of toks) {
      const variants = expand(raw);
      let best = 0;
      for (const t of variants) {
        if (title.includes(t)) best = Math.max(best, title.startsWith(t) ? 6 : 5);
        if (topics.some((x) => x.includes(t))) best = Math.max(best, 3);
        if (summary.includes(t)) best = Math.max(best, 2);
        else if (body.includes(t)) best = Math.max(best, 1);
      }
      if (best === 0) matchedAll = false;
      s += best;
    }
    if (!matchedAll) return { s: 0, hit: null };
    return { s, hit: toks };
  }

  function snippet(n, toks) {
    const text = n.body_text || n.summary || "";
    const low = fold(text);
    let idx = -1;
    for (const raw of toks) {
      for (const t of expand(raw)) {
        const i = low.indexOf(t);
        if (i !== -1 && (idx === -1 || i < idx)) idx = i;
      }
      if (idx !== -1) break;
    }
    if (idx === -1) return "";
    const start = Math.max(0, idx - 40);
    let frag = text.slice(start, start + 160).trim();
    if (start > 0) frag = "… " + frag;
    frag = escapeHtml(frag);
    for (const raw of toks) {
      for (const t of expand(raw)) {
        if (t.length < 2) continue;
        const re = new RegExp("(" + t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "ig");
        frag = frag.replace(re, "<mark>$1</mark>");
      }
    }
    return frag;
  }

  function matched() {
    const toks = tokenize(query);
    return notes
      .map((n) => ({ n, ...scoreNote(n, toks) }))
      .filter((x) => x.s > 0)
      .sort((a, b) => b.s - a.s || a.n.title.localeCompare(b.n.title));
  }

  // ---- render ------------------------------------------------------------ //
  function badge(on, label) {
    return `<span class="badge ${on ? "on" : ""}">${label}</span>`;
  }

  function rowHtml(n, toks) {
    const snip = toks && toks.length ? snippet(n, toks) : "";
    return `
      <a class="row" href="${escapeHtml(n.page)}">
        <div class="row-top">
          <h3>${escapeHtml(n.title)}</h3>
          <span class="spacer"></span>
          <span class="badges">
            ${badge(!!n.slides, "slides")}
            ${badge(!!n.demo, "demo")}
          </span>
        </div>
        <p>${escapeHtml(n.summary)}</p>
        ${snip ? `<div class="snippet">${snip}</div>` : ""}
        <div class="topics">${(n.topics || []).slice(0, 5).map((t) => `<span>#${escapeHtml(t)}</span>`).join("")}</div>
      </a>`;
  }

  function followup(toks) {
    // suggest related topics / notes from the whole catalog
    const all = new Map();
    for (const n of notes) for (const t of n.topics || []) all.set(t, (all.get(t) || 0) + 1);
    const suggestions = [...all.keys()].filter((t) => {
      const ft = fold(t);
      return !toks.some((q) => ft.includes(q) || q.includes(ft));
    }).slice(0, 8);
    const chips = suggestions.map((t) => `<button type="button" data-chip="${escapeHtml(t)}">${escapeHtml(t)}</button>`).join("");
    return `
      <div class="followup">
        <h4>Ít kết quả cho “${escapeHtml(query)}”.</h4>
        <p>Search chỉ quét <strong>notes</strong> (không phải video/GitHub — xem note Personal Knowledge-base). Thử thu hẹp hoặc chọn một hướng liên quan:</p>
        <div class="chips">${chips}</div>
      </div>`;
  }

  function render() {
    const toks = tokenize(query);
    const rows = matched();
    document.getElementById("metaLine").textContent =
      `${rows.length}/${notes.length} notes · search = notes only · built ${payload.built_at || "?"}`;

    let html = "";
    if (query.trim()) {
      // flat ranked list with snippets
      html = rows.length
        ? `<div class="list">${rows.map((x) => rowHtml(x.n, toks)).join("")}</div>`
        : `<p class="empty">Không có note khớp.</p>`;
      if (rows.length < 2) html += followup(toks);
    } else {
      // flat browse list in catalog order
      html = notes.length
        ? `<div class="list">${notes.map((n) => rowHtml(n, null)).join("")}</div>`
        : `<p class="empty">Chưa có note.</p>`;
    }
    document.getElementById("results").innerHTML = html;
  }

  // ---- events ------------------------------------------------------------ //
  const qEl = document.getElementById("q");
  document.getElementById("searchForm").addEventListener("submit", (e) => e.preventDefault());
  qEl.addEventListener("input", (e) => {
    query = e.target.value;
    const u = new URL(location);
    if (query) u.searchParams.set("q", query); else u.searchParams.delete("q");
    history.replaceState(null, "", u);
    render();
  });
  document.getElementById("results").addEventListener("click", (e) => {
    const chip = e.target.closest("button[data-chip]");
    if (chip) {
      query = chip.dataset.chip;
      qEl.value = query;
      const u = new URL(location); u.searchParams.set("q", query); history.replaceState(null, "", u);
      render();
      qEl.focus();
    }
  });

  document.getElementById("foot").textContent = "Build: python3 scripts/build-docs.py — source: notes/*.md + catalog.json";

  // deep link ?q= and ?note=
  const params = new URLSearchParams(location.search);
  if (params.get("note")) {
    const n = notes.find((x) => x.id === params.get("note"));
    if (n) { location.replace(n.page); return; }
  }
  if (params.get("q")) { query = params.get("q"); qEl.value = query; }

  render();
  qEl.focus();
})();
</script>
</body>
</html>
"""


# --------------------------------------------------------------------------- #
# Note page template                                                          #
# --------------------------------------------------------------------------- #
NOTE_HTML = r"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>@@TITLE@@ · AI Lab</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&family=Sora:wght@400;500;600;700&display=swap" rel="stylesheet" />
<style>
@@THEME@@
.wrap { max-width: 740px; margin: 0 auto; padding: 32px 22px 96px; }
.back { display: inline-flex; align-items: center; gap: 7px; text-decoration: none; color: var(--muted); font: 500 13px var(--mono); }
.back:hover { color: var(--teal); }
.doc {
  background: var(--surface); border: 1px solid var(--line); border-radius: 18px;
  padding: 34px 36px 44px; margin-top: 18px; box-shadow: var(--shadow);
}
.grp { font: 500 11px var(--mono); letter-spacing: .16em; text-transform: uppercase; color: var(--teal); }
.doc h1 { font-size: 30px; letter-spacing: -.02em; margin: 8px 0 6px; }
.summary { color: var(--muted); font-size: 15px; line-height: 1.55; }
.actions { display: flex; flex-wrap: wrap; gap: 8px; margin: 18px 0 4px; }
.actions a, .actions button {
  text-decoration: none; font: 500 12px var(--mono); padding: 9px 14px; border-radius: 10px;
  border: 1px solid var(--line); color: var(--ink); background: transparent; transition: all .15s;
  cursor: pointer;
}
.actions a.primary { background: var(--teal); border-color: var(--teal); color: #fff; }
.actions a:hover, .actions button:hover { border-color: var(--teal); color: var(--teal); }
.actions a.primary:hover { color: #fff; opacity: .9; }
.lab-toast {
  position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%);
  background: var(--ink); color: #fff; font: 500 12px var(--mono);
  padding: 10px 16px; border-radius: 999px; z-index: 1100;
  opacity: 0; pointer-events: none; transition: opacity .2s;
}
.lab-toast.on { opacity: 1; }
.topics { display: flex; flex-wrap: wrap; gap: 7px; margin: 14px 0 4px; }
.topics span { font: 500 11px var(--mono); color: var(--amber); }
hr.sep { border: none; border-top: 1px solid var(--line-soft); margin: 22px 0; }
.body h1 { font-size: 24px; margin: 1.2em 0 .5em; }
.body h2 { font-size: 19px; margin: 1.4em 0 .5em; letter-spacing: -.01em; }
.body h3 { font-size: 16px; margin: 1.2em 0 .4em; }
.body p, .body li { color: #2b3a4d; line-height: 1.65; font-size: 15px; }
.body ul { padding-left: 1.25em; margin: .5em 0 1em; }
.body li { margin: .25em 0; }
.body a { color: var(--teal); text-decoration: none; border-bottom: 1px solid var(--teal-soft); }
.body a:hover { border-color: var(--teal); }
.body code { font-family: var(--mono); font-size: 13px; color: var(--amber); background: rgba(194,112,58,.09); padding: 1px 5px; border-radius: 5px; }
.body pre { background: #0f1720; border-radius: 12px; padding: 16px; overflow: auto; margin: 14px 0; }
.body pre code { color: #dbe6f2; background: none; padding: 0; font-size: 12.5px; line-height: 1.6; }
.body blockquote { border-left: 3px solid var(--teal); background: var(--teal-soft); padding: 10px 16px; margin: 14px 0; border-radius: 0 8px 8px 0; color: var(--ink); }
.body table { width: 100%; border-collapse: collapse; margin: 14px 0; font-size: 13.5px; }
.body th, .body td { border: 1px solid var(--line); padding: 9px 11px; text-align: left; color: #2b3a4d; }
.body th { color: var(--teal); font: 500 11px var(--mono); letter-spacing: .05em; text-transform: uppercase; background: var(--teal-soft); }
</style>
</head>
<body>
<div class="wrap">
  <a class="back" href="../index.html">
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="m15 18-6-6 6-6"/></svg>
    AI Lab
  </a>
  <article class="doc">
    <h1>@@TITLE@@</h1>
    <p class="summary">@@SUMMARY@@</p>
    <div class="actions">@@ACTIONS@@</div>
    <div class="topics">@@TOPICS@@</div>
    <hr class="sep" />
    <div class="body">@@BODY@@</div>
  </article>
</div>
<script>
(function () {
  const title = @@TITLE_JS@@;
  function toast(msg) {
    let el = document.querySelector(".lab-toast");
    if (!el) { el = document.createElement("div"); el.className = "lab-toast"; document.body.appendChild(el); }
    el.textContent = msg; el.classList.add("on");
    clearTimeout(el._t); el._t = setTimeout(() => el.classList.remove("on"), 1600);
  }
  document.getElementById("labShare")?.addEventListener("click", async () => {
    const url = location.href;
    try { if (navigator.share) { await navigator.share({ title, url }); return; } }
    catch (err) { if (err && err.name === "AbortError") return; }
    try { await navigator.clipboard.writeText(url); toast("Copied link"); }
    catch { window.prompt("Copy link:", url); }
  });
})();
</script>
</body>
</html>
"""


def esc(s: str) -> str:
    return (
        str(s or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render_note_page(n: dict) -> str:
    actions = []
    if n.get("slides"):
        actions.append(f'<a class="primary" href="{esc(n["slides"])}">Slides ↗</a>')
    if n.get("demo"):
        actions.append(f'<a href="{esc(n["demo"])}">Demo ↗</a>')
    # download = raw.md (copied next to the page); share = current URL
    raw_name = posixpath.basename(n["raw"])
    actions.append(f'<a href="{esc(raw_name)}" id="labDownload" download="{esc(raw_name)}">Download</a>')
    actions.append('<button type="button" id="labShare">Share</button>')
    for l in n.get("extra_links") or []:
        actions.append(f'<a href="{esc(l["href"])}">{esc(l["label"])} ↗</a>')
    topics = "".join(f"<span>#{esc(t)}</span>" for t in n.get("topics") or [])
    title_js = json.dumps(n["title"], ensure_ascii=False)
    return (
        NOTE_HTML.replace("@@THEME@@", THEME_CSS)
        .replace("@@TITLE@@", esc(n["title"]))
        .replace("@@SUMMARY@@", esc(n["summary"]))
        .replace("@@ACTIONS@@", "\n".join(actions))
        .replace("@@TOPICS@@", topics)
        .replace("@@BODY@@", n["body_html"])
        .replace("@@TITLE_JS@@", title_js)
    )


def render_hub(payload: dict) -> str:
    data = json.dumps(payload, ensure_ascii=False).replace("<", "\\u003c")
    return HUB_HTML.replace("@@THEME@@", THEME_CSS).replace("@@NOTES_JSON@@", data)


# --------------------------------------------------------------------------- #
# Asset copy + demos/slides chrome (download / share)                          #
# --------------------------------------------------------------------------- #
def copy_assets() -> None:
    # top-level dirs copied verbatim into docs/
    for name in ("demos", "slides"):
        src = ROOT / name
        if not src.is_dir():
            continue
        dst = DOCS / name
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".DS_Store"))

    # note assets (protonx images) → docs/notes/assets so both note pages and
    # decks (which point at ../../../notes/assets/...) resolve inside docs/.
    assets_src = ROOT / "notes" / "assets"
    if assets_src.is_dir():
        assets_dst = NOTES_OUT / "assets"
        if assets_dst.exists():
            shutil.rmtree(assets_dst)
        shutil.copytree(assets_src, assets_dst, ignore=shutil.ignore_patterns(".DS_Store"))


def _inject_before_body_end(html: str, snippet: str) -> str:
    if snippet.strip() in html:
        return html
    if "</body>" in html:
        return html.replace("</body>", snippet + "\n</body>", 1)
    return html + snippet


def _make_standalone_slide(index_html: Path, shared: Path) -> str:
    """Inline deck.css + deck.js into one static HTML file for Download."""
    html = index_html.read_text(encoding="utf-8")
    css = (shared / "deck.css").read_text(encoding="utf-8")
    js = (shared / "deck.js").read_text(encoding="utf-8")

    html = re.sub(
        r'<link[^>]+href="[^"]*deck\.css"[^>]*/?>',
        f"<style>\n{css}\n</style>",
        html,
        count=1,
    )
    # drop external deck.js; LAB + inlined deck.js appended before </body>
    html = re.sub(r'<script[^>]+src="[^"]*deck\.js"[^>]*>\s*</script>', "", html)
    html = re.sub(r'<script[^>]+src="[^"]*deck\.js"[^>]*/>', "", html)

    # keep window.LAB if already present; else add a minimal one for share-only
    lab_snip = ""
    if "window.LAB" not in html:
        title = re.search(r"<title>([^<]+)</title>", html)
        t = title.group(1).strip() if title else "AI Lab Slides"
        lab_snip = f"<script>window.LAB={json.dumps({'title': t, 'download': 'download.html', 'downloadName': index_html.parent.name + '-slides.html'})};</script>\n"

    inline = f"{lab_snip}<script>\n{js}\n</script>\n"
    return _inject_before_body_end(html, inline)


def _zip_demo(demo_dir: Path, zip_path: Path, shared: Path | None = None) -> None:
    """Zip one demo folder (app + slides + readme) + shared assets for Download."""
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(demo_dir.rglob("*")):
            if not f.is_file():
                continue
            if f.name == ".DS_Store" or f.suffix == ".zip":
                continue
            if f.name == "download.html":
                continue
            arc = f"{demo_dir.name}/{f.relative_to(demo_dir).as_posix()}"
            zf.write(f, arc)
        # apps/slides resolve ../../_shared from demo/app → include sibling _shared/
        if shared and shared.is_dir():
            for f in sorted(shared.rglob("*")):
                if not f.is_file() or f.name == ".DS_Store":
                    continue
                zf.write(f, f"_shared/{f.relative_to(shared).as_posix()}")


def enhance_demos_and_slides() -> None:
    """After copy: inject Download/Share, build standalone slides, zip demos.

    Layout (sibling trees):
        docs/demos/<id>/app/     working apps
        docs/slides/<id>/        decks (shared CSS/JS in docs/slides/_shared/)
    """
    demos_root = DOCS / "demos"
    slides_root = DOCS / "slides"
    demo_shared = demos_root / "_shared"
    slide_shared = slides_root / "_shared"

    # --- demos: chrome + zip ---
    if demos_root.is_dir():
        for demo_dir in sorted(demos_root.iterdir()):
            if not demo_dir.is_dir() or demo_dir.name.startswith("_"):
                continue
            demo_id = demo_dir.name
            title = demo_id.replace("-", " ").title()
            zip_name = f"{demo_id}.zip"

            app_html = demo_dir / "app" / "index.html"
            if app_html.is_file():
                lab = {
                    "kind": "app",
                    "title": f"{title} · Demo",
                    "download": f"../{zip_name}",
                    "downloadName": zip_name,
                }
                snip = (
                    f"<script>window.LAB={json.dumps(lab, ensure_ascii=False)};</script>\n"
                    f'<script src="../../_shared/chrome.js"></script>\n'
                )
                text = app_html.read_text(encoding="utf-8")
                if "window.LAB" not in text:
                    app_html.write_text(_inject_before_body_end(text, snip), encoding="utf-8")

            _zip_demo(
                demo_dir,
                demo_dir / zip_name,
                demo_shared if demo_shared.is_dir() else None,
            )

    # --- slides/<id>/index.html: Download (standalone HTML) + Share ---
    if slides_root.is_dir() and slide_shared.is_dir():
        for slide_dir in sorted(slides_root.iterdir()):
            if not slide_dir.is_dir() or slide_dir.name.startswith("_"):
                continue
            slides_html = slide_dir / "index.html"
            if not slides_html.is_file():
                continue
            slide_id = slide_dir.name
            title = slide_id.replace("-", " ").title()
            lab = {
                "kind": "slides",
                "title": f"{title} · Slides",
                "download": "download.html",
                "downloadName": f"{slide_id}-slides.html",
            }
            lab_script = f"<script>window.LAB={json.dumps(lab, ensure_ascii=False)};</script>\n"
            text = slides_html.read_text(encoding="utf-8")
            if "window.LAB" not in text:
                if re.search(r'src="[^"]*deck\.js"', text):
                    text = re.sub(
                        r'(<script[^>]+src="[^"]*deck\.js"[^>]*>)',
                        lab_script + r"\1",
                        text,
                        count=1,
                    )
                else:
                    text = _inject_before_body_end(text, lab_script)
                slides_html.write_text(text, encoding="utf-8")

            standalone = _make_standalone_slide(slides_html, slide_shared)
            (slide_dir / "download.html").write_text(standalone, encoding="utf-8")


# --------------------------------------------------------------------------- #
# Main                                                                         #
# --------------------------------------------------------------------------- #
def main() -> None:
    payload, page_notes = build_payload()

    NOTES_OUT.mkdir(parents=True, exist_ok=True)
    (DOCS / "search-index.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (DOCS / "index.html").write_text(render_hub(payload), encoding="utf-8")

    for n in page_notes:
        (NOTES_OUT / f"{n['id']}.html").write_text(render_note_page(n), encoding="utf-8")
        # copy source .md next to the page for Download
        src = ROOT / n["raw_src"]
        if src.is_file():
            shutil.copy2(src, NOTES_OUT / n["raw"])

    copy_assets()
    enhance_demos_and_slides()

    print(f"OK {len(page_notes)} notes")
    print(f"    hub        → {DOCS / 'index.html'}")
    print(f"    note pages → {NOTES_OUT}/<id>.html")
    print(f"    copied     → docs/demos, docs/slides (+ zip / download.html)")
    print(f"    built_at   {payload['built_at']}")


if __name__ == "__main__":
    main()
