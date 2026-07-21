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
JOURNEY = ROOT / "notes" / "journey.json"
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
    # images before links (![alt](src) must not be caught by the link rule)
    s = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1" loading="lazy" />', s)
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

        # Tables may be indented (nested under a list item)
        stripped = line.strip()
        if re.match(r"^\|", stripped) and "|" in stripped[1:]:
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if all(re.match(r"^:?-+:?$", c.replace(" ", "")) for c in cells):
                continue
            if not in_table:
                close_ul()
                out.append("<table><thead>")
                in_table = True
                out.append("<tr>" + "".join(f"<th>{inline(c)}</th>" for c in cells) + "</tr>")
                out.append("</thead><tbody>")
            else:
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>")
            continue
        else:
            close_table()

        m = re.match(r"^(#{1,3})\s+(.*)$", stripped)
        if m:
            close_ul()
            level = len(m.group(1))
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            continue

        if re.match(r"^[-*]\s+", stripped):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            item = re.sub(r"^[-*]\s+", "", stripped)
            out.append(f"<li>{inline(item)}</li>")
            continue
        else:
            close_ul()

        if not stripped:
            continue
        # standalone image on its own line → figure + caption (alt text)
        mimg = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", stripped)
        if mimg:
            close_ul()
            alt = inline(mimg.group(1)) if mimg.group(1) else ""
            src = mimg.group(2)
            cap = f"<figcaption>{alt}</figcaption>" if alt else ""
            out.append(f'<figure><img src="{src}" alt="{mimg.group(1)}" loading="lazy" />{cap}</figure>')
            continue
        if stripped.startswith(">"):
            out.append(f"<blockquote>{inline(stripped.lstrip('> ').strip())}</blockquote>")
            continue
        out.append(f"<p>{inline(stripped)}</p>")

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
def _auto_date(i: int, total: int) -> str:
    """Auto-assign a month/year spread evenly across Jan 2023 → Jul 2026.

    Not meant to be accurate — just a stable, increasing timeline label so the
    listing reads like a learning journey from 2023 to now.
    """
    start_m = 2023 * 12 + 0  # Jan 2023
    end_m = 2026 * 12 + 6  # Jul 2026
    span = max(1, total - 1)
    m = round(start_m + (end_m - start_m) * i / span)
    year, month = divmod(m, 12)
    return f"{month + 1:02d}/{year}"


def build_payload() -> tuple[dict, list[dict]]:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    entries = catalog["notes"]
    file2id = {posixpath.basename(e["file"]): e["id"] for e in entries}
    # Auto numbers/dates; optional catalog overrides via `num` / `date`.
    content_total = sum(1 for e in entries if e.get("num") is None)

    search_notes: list[dict] = []
    page_notes: list[dict] = []

    content_i = -1
    for entry in entries:
        if entry.get("num") is not None:
            num = str(entry["num"])
            date = entry.get("date") or "—"
        else:
            content_i += 1
            num = f"{content_i + 1:02d}"
            date = entry.get("date") or _auto_date(content_i, content_total)
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
                "num": num,
                "date": date,
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
                "num": num,
                "date": date,
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
# Shared theme (light / dark via data-theme; system resolved in JS)             #
# --------------------------------------------------------------------------- #
THEME_CSS = r"""
:root, [data-theme="light"] {
  --bg: #eef3f9; --surface: #ffffff; --ink: #16202e; --muted: #5a6b80;
  --teal: #0f8a9b; --teal-soft: rgba(15,138,155,.12); --amber: #c2703a;
  --line: rgba(20,32,46,.12); --line-soft: rgba(20,32,46,.07);
  --shadow: 0 1px 2px rgba(20,32,46,.05), 0 8px 24px rgba(20,32,46,.06);
  --glow-teal: rgba(15,138,155,.10); --glow-amber: rgba(194,112,58,.08);
  --font: Sora, system-ui, sans-serif; --serif: "Instrument Serif", Georgia, serif;
  --mono: "IBM Plex Mono", ui-monospace, monospace;
}
[data-theme="dark"] {
  --bg: #0d1520; --surface: #152033; --ink: #e8eef6; --muted: #8b9bb0;
  --teal: #3db8c9; --teal-soft: rgba(61,184,201,.16); --amber: #d4894a;
  --line: rgba(232,238,246,.12); --line-soft: rgba(232,238,246,.07);
  --shadow: 0 1px 2px rgba(0,0,0,.25), 0 8px 24px rgba(0,0,0,.35);
  --glow-teal: rgba(61,184,201,.12); --glow-amber: rgba(212,137,74,.10);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  min-height: 100vh; color: var(--ink); font-family: var(--font);
  background:
    radial-gradient(ellipse 60% 45% at 88% -5%, var(--glow-teal), transparent 60%),
    radial-gradient(ellipse 55% 45% at 0% 105%, var(--glow-amber), transparent 55%),
    var(--bg);
  -webkit-font-smoothing: antialiased;
}
a { color: var(--teal); }
::selection { background: var(--teal-soft); }
.logo-light, .logo-dark { height: 64px; width: auto; max-width: min(420px, 100%); object-fit: contain; object-position: left center; }
.logo-light { display: block; }
.logo-dark { display: none; }
[data-theme="dark"] .logo-light { display: none; }
[data-theme="dark"] .logo-dark { display: block; }
.theme-bar, .lang-bar {
  display: inline-flex; gap: 2px; padding: 3px;
  background: var(--surface); border: 1px solid var(--line); border-radius: 999px;
  box-shadow: var(--shadow);
}
.theme-bar button, .lang-bar button {
  appearance: none; border: 0; background: transparent; color: var(--muted);
  width: 34px; height: 30px; padding: 0; border-radius: 999px; cursor: pointer;
  display: inline-flex; align-items: center; justify-content: center; transition: all .15s;
}
.theme-bar button:hover, .lang-bar button:hover { color: var(--teal); }
.theme-bar button.on, .lang-bar button.on { background: var(--teal); color: #fff; }
.theme-bar button svg, .lang-bar button svg { width: 15px; height: 15px; display: block; }
.lang-bar .lang-mark { font: 700 11px var(--mono); line-height: 1; letter-spacing: .02em; }
.prefs { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
html.i18n-busy { cursor: progress; }
html.i18n-busy .lang-bar { opacity: .7; pointer-events: none; }
"""

# Runs in <head> before paint — prevents flash of wrong theme.
THEME_BOOT = r"""<script>
(function () {
  try {
    var KEY = "ai-lab-theme";
    var pref = localStorage.getItem(KEY) || "system";
    if (pref !== "light" && pref !== "dark" && pref !== "system") pref = "system";
    var dark = pref === "dark" || (pref === "system" && window.matchMedia("(prefers-color-scheme: dark)").matches);
    document.documentElement.setAttribute("data-theme", dark ? "dark" : "light");
    document.documentElement.setAttribute("data-theme-pref", pref);
  } catch (e) {
    document.documentElement.setAttribute("data-theme", "light");
    document.documentElement.setAttribute("data-theme-pref", "system");
  }
})();
</script>"""

LANG_BOOT = r"""<script>
(function () {
  try {
    var KEY = "ai-lab-lang";
    var pref = localStorage.getItem(KEY) || "system";
    if (pref !== "en" && pref !== "vi" && pref !== "system") pref = "system";
    var nav = String(navigator.language || "en").toLowerCase();
    var resolved = pref === "system" ? (nav.indexOf("vi") === 0 ? "vi" : "en") : pref;
    document.documentElement.setAttribute("data-lang-pref", pref);
    document.documentElement.setAttribute("data-lang", resolved);
    document.documentElement.lang = resolved;
  } catch (e) {
    document.documentElement.setAttribute("data-lang-pref", "system");
    document.documentElement.setAttribute("data-lang", "en");
    document.documentElement.lang = "en";
  }
})();
</script>"""

THEME_CTRL = r"""
<div class="theme-bar" role="group" aria-label="Theme" translate="no">
  <button type="button" data-theme-set="light" aria-label="Light" title="Light"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg></button>
  <button type="button" data-theme-set="system" aria-label="System" title="System"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/></svg></button>
  <button type="button" data-theme-set="dark" aria-label="Dark" title="Dark"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 14.5A8.5 8.5 0 1 1 9.5 3a6.8 6.8 0 0 0 11.5 11.5z"/></svg></button>
</div>
<script>
(function () {
  var KEY = "ai-lab-theme";
  function resolve(pref) {
    if (pref === "light" || pref === "dark") return pref;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  function apply(pref) {
    if (pref !== "light" && pref !== "dark" && pref !== "system") pref = "system";
    var resolved = resolve(pref);
    document.documentElement.setAttribute("data-theme", resolved);
    document.documentElement.setAttribute("data-theme-pref", pref);
    try { localStorage.setItem(KEY, pref); } catch (e) {}
    document.querySelectorAll("[data-theme-set]").forEach(function (btn) {
      btn.classList.toggle("on", btn.getAttribute("data-theme-set") === pref);
    });
  }
  var pref = document.documentElement.getAttribute("data-theme-pref") || "system";
  apply(pref);
  document.querySelectorAll("[data-theme-set]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      apply(btn.getAttribute("data-theme-set"));
    });
  });
  try {
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function () {
      var p = document.documentElement.getAttribute("data-theme-pref") || "system";
      if (p === "system") apply("system");
    });
  } catch (e) {}
})();
</script>
"""

# Dynamic EN→VI via public web translate API. Source pages stay English-only.
LANG_CTRL = r"""
<div class="lang-bar" role="group" aria-label="Language" translate="no">
  <button type="button" data-lang-set="en" aria-label="English" title="English"><span class="lang-mark">A</span></button>
  <button type="button" data-lang-set="system" aria-label="System" title="System"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg></button>
  <button type="button" data-lang-set="vi" aria-label="Tiếng Việt" title="Tiếng Việt"><span class="lang-mark">V</span></button>
</div>
<script>
(function () {
  var KEY = "ai-lab-lang";
  var CACHE_KEY = "ai-lab-i18n-en-vi";
  var SKIP = /^(SCRIPT|STYLE|NOSCRIPT|CODE|PRE|KBD|SAMP|TEXTAREA|SVG|MATH)$/;
  var cache = {};
  try { cache = JSON.parse(localStorage.getItem(CACHE_KEY) || "{}") || {}; } catch (e) { cache = {}; }

  function resolve(pref) {
    if (pref === "en" || pref === "vi") return pref;
    var nav = String(navigator.language || "en").toLowerCase();
    return nav.indexOf("vi") === 0 ? "vi" : "en";
  }

  function saveCache() {
    try { localStorage.setItem(CACHE_KEY, JSON.stringify(cache)); } catch (e) {}
  }

  async function translateOne(text) {
    if (!text || !text.trim()) return text;
    if (cache[text]) return cache[text];
    // Google gtx web endpoint (no API key). Fallback: MyMemory.
    var q = encodeURIComponent(text);
    try {
      var url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=vi&dt=t&q=" + q;
      var res = await fetch(url);
      if (res.ok) {
        var data = await res.json();
        var out = (data[0] || []).map(function (row) { return row[0] || ""; }).join("");
        if (out) { cache[text] = out; return out; }
      }
    } catch (e) {}
    try {
      var url2 = "https://api.mymemory.translated.net/get?langpair=en|vi&q=" + q;
      var res2 = await fetch(url2);
      if (res2.ok) {
        var data2 = await res2.json();
        var out2 = data2 && data2.responseData && data2.responseData.translatedText;
        if (out2 && out2.indexOf("MYMEMORY WARNING") === -1) {
          cache[text] = out2;
          return out2;
        }
      }
    } catch (e2) {}
    return text;
  }

  function collectNodes(root) {
    var out = [];
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        if (!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        var el = node.parentElement;
        if (!el) return NodeFilter.FILTER_REJECT;
        if (el.closest("[translate=no], .notranslate, .theme-bar, .lang-bar, .prefs, code, pre, kbd, samp")) {
          return NodeFilter.FILTER_REJECT;
        }
        if (SKIP.test(el.tagName)) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    while (walker.nextNode()) out.push(walker.currentNode);
    return out;
  }

  async function mapPool(items, limit, fn) {
    var i = 0;
    var workers = [];
    async function worker() {
      while (i < items.length) {
        var idx = i++;
        items[idx].result = await fn(items[idx].src);
      }
    }
    for (var w = 0; w < Math.min(limit, items.length); w++) workers.push(worker());
    await Promise.all(workers);
  }

  async function applyLang(pref) {
    if (pref !== "en" && pref !== "vi" && pref !== "system") pref = "system";
    var resolved = resolve(pref);
    document.documentElement.setAttribute("data-lang-pref", pref);
    document.documentElement.setAttribute("data-lang", resolved);
    document.documentElement.lang = resolved;
    try { localStorage.setItem(KEY, pref); } catch (e) {}
    document.querySelectorAll("[data-lang-set]").forEach(function (btn) {
      btn.classList.toggle("on", btn.getAttribute("data-lang-set") === pref);
    });

    var nodes = collectNodes(document.body);
    nodes.forEach(function (node) {
      if (node._i18nEn == null) node._i18nEn = node.nodeValue;
    });

    if (resolved === "en") {
      nodes.forEach(function (node) {
        if (node._i18nEn != null) node.nodeValue = node._i18nEn;
      });
      return;
    }

    document.documentElement.classList.add("i18n-busy");
    try {
      var jobs = nodes.map(function (node) {
        return { node: node, src: node._i18nEn };
      });
      await mapPool(jobs, 4, translateOne);
      jobs.forEach(function (job) {
        job.node.nodeValue = job.result;
      });
      saveCache();
    } finally {
      document.documentElement.classList.remove("i18n-busy");
    }
  }

  var pref = document.documentElement.getAttribute("data-lang-pref") || "system";
  document.querySelectorAll("[data-lang-set]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      applyLang(btn.getAttribute("data-lang-set"));
    });
  });
  // Defer first translate so DOM is ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () { applyLang(pref); });
  } else {
    applyLang(pref);
  }
})();
</script>
"""

PREFS_CTRL = (
    '<div class="prefs" translate="no">\n'
    + THEME_CTRL[: THEME_CTRL.index("<script>")].strip()
    + "\n"
    + LANG_CTRL[: LANG_CTRL.index("<script>")].strip()
    + "\n</div>\n"
    + THEME_CTRL[THEME_CTRL.index("<script>") :]
    + "\n"
    + LANG_CTRL[LANG_CTRL.index("<script>") :]
)


# --------------------------------------------------------------------------- #
# Hub template                                                                 #
# --------------------------------------------------------------------------- #
HUB_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>AI Lab</title>
@@THEME_BOOT@@
@@LANG_BOOT@@
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&family=Sora:wght@400;500;600;700&display=swap" rel="stylesheet" />
<style>
@@THEME@@
.shell { max-width: 880px; margin: 0 auto; padding: 56px 22px 96px; }
.top-row { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; flex-wrap: wrap; }
.brand {
  display: block; text-decoration: none; color: inherit;
  line-height: 0;
}
.tagline { margin-top: 14px; color: var(--muted); font-size: 15px; max-width: 560px; line-height: 1.5; }
.journey-cta {
  display: flex; align-items: center; gap: 16px; flex-wrap: wrap;
  margin: 18px 0 0; padding: 16px 18px; text-decoration: none; color: inherit;
  background: linear-gradient(120deg, rgba(15,138,155,.10), var(--surface) 55%);
  border: 1px solid var(--teal); border-radius: 16px; box-shadow: var(--shadow);
  transition: transform .15s, box-shadow .15s;
}
#results { margin-top: 32px; padding-top: 8px; }
.journey-cta:hover { transform: translateY(-1px); box-shadow: 0 8px 28px rgba(15,138,155,.14); }
.journey-cta .j-kicker {
  font: 600 11px var(--mono); letter-spacing: .14em; text-transform: uppercase; color: var(--teal);
}
.journey-cta .j-title { font-size: 17px; font-weight: 600; margin-top: 2px; }
.journey-cta .j-sub { color: var(--muted); font-size: 13px; margin-top: 4px; line-height: 1.45; }
.journey-cta .j-go {
  margin-left: auto; font: 600 12px var(--mono); color: #fff; background: var(--teal);
  padding: 10px 14px; border-radius: 999px; white-space: nowrap;
}
.search-wrap { position: relative; margin: 22px 0 10px; }
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
.row-date { font: 500 11px var(--mono); letter-spacing: .08em; color: var(--amber); margin-bottom: 6px; }
.row-num {
  font: 600 11px var(--mono); letter-spacing: .05em; color: var(--teal);
  background: var(--teal-soft); border-radius: 7px; padding: 3px 8px; align-self: center;
}
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
  <div class="top-row">
    <a class="brand" href="./index.html" aria-label="AI Lab">
      <img class="logo-light" src="notes/assets/ai-lab-logo-light.png" alt="AI Lab" width="420" height="120" />
      <img class="logo-dark" src="notes/assets/ai-lab-logo-dark.png" alt="AI Lab" width="420" height="120" />
    </a>
    @@THEME_CTRL@@
  </div>
  <p class="tagline">Notes are the source of truth. Search first — open a note as a document; slides &amp; demos appear when available.</p>
  <div data-lab-stack></div>

  <form class="search-wrap" id="searchForm" autocomplete="off">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
    <input id="q" type="search" placeholder="Search: tokenize, rag, mcp, skills, grok…" />
  </form>
  <p class="meta-line" id="metaLine">Loading…</p>

  <a class="journey-cta" href="journey.html">
    <div>
      <div class="j-kicker">Journey · not a note</div>
      <div class="j-title">5 stages · a fun AI Lab map</div>
      <div class="j-sub">ABC of text → build/train → RAG → demo → agent. Pick a path by mood.</div>
    </div>
    <span class="j-go">Open journey →</span>
  </a>

  <div id="results"></div>

  <footer id="foot"></footer>
</div>

<script src="_shared/nav-stack.js"></script>
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
        ${n.date ? `<div class="row-date">${escapeHtml(n.date)}</div>` : ""}
        <div class="row-top">
          ${n.num ? `<span class="row-num">${escapeHtml(n.num)}</span>` : ""}
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
        <h4>Few hits for “${escapeHtml(query)}”.</h4>
        <p>Search only covers <strong>notes</strong> (not videos/GitHub — see the Personal Knowledge-base note). Try a narrower query or pick a related topic:</p>
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
        : `<p class="empty">No matching notes.</p>`;
      if (rows.length < 2) html += followup(toks);
    } else {
      // flat browse list in catalog order
      html = notes.length
        ? `<div class="list">${notes.map((n) => rowHtml(n, null)).join("")}</div>`
        : `<p class="empty">No notes yet.</p>`;
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

  document.getElementById("foot").textContent = "Build: ./scripts/build.sh — source: notes/*.md + catalog.json";

  // deep link ?q= and ?note=
  const params = new URLSearchParams(location.search);
  if (params.get("note")) {
    const n = notes.find((x) => x.id === params.get("note"));
    if (n) { location.replace(n.page); return; }
  }
  if (params.get("q")) { query = params.get("q"); qEl.value = query; }

  render();
  if (window.AiLabNav) {
    AiLabNav.enter("Home");
  }
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
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>@@TITLE@@ · AI Lab</title>
@@THEME_BOOT@@
@@LANG_BOOT@@
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&family=Sora:wght@400;500;600;700&display=swap" rel="stylesheet" />
<style>
@@THEME@@
.wrap { max-width: 960px; margin: 0 auto; padding: 32px 22px 96px; }
.nav-row { display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
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
.body p, .body li { color: var(--ink); line-height: 1.65; font-size: 15px; opacity: .92; }
.body ul { padding-left: 1.25em; margin: .5em 0 1em; }
.body li { margin: .25em 0; }
.body a { color: var(--teal); text-decoration: none; border-bottom: 1px solid var(--teal-soft); }
.body a:hover { border-color: var(--teal); }
.body code { font-family: var(--mono); font-size: 13px; color: var(--amber); background: rgba(194,112,58,.09); padding: 1px 5px; border-radius: 5px; }
.body pre { background: #0f1720; border-radius: 12px; padding: 16px; overflow: auto; margin: 14px 0; }
.body pre code { color: #dbe6f2; background: none; padding: 0; font-size: 12.5px; line-height: 1.6; }
.body blockquote { border-left: 3px solid var(--teal); background: var(--teal-soft); padding: 10px 16px; margin: 14px 0; border-radius: 0 8px 8px 0; color: var(--ink); }
.body table { width: 100%; border-collapse: collapse; margin: 14px 0; font-size: 13.5px; }
.body th, .body td { border: 1px solid var(--line); padding: 9px 11px; text-align: left; color: var(--ink); }
.body th { color: var(--teal); font: 500 11px var(--mono); letter-spacing: .05em; text-transform: uppercase; background: var(--teal-soft); }
.body figure { margin: 20px 0; }
.body figure img { width: 100%; height: auto; display: block; border-radius: 12px; border: 1px solid var(--line); background: #e6edf5; }
.body figcaption { font: 500 12px var(--mono); color: var(--muted); margin-top: 8px; text-align: center; }
.body p img { max-width: 100%; height: auto; border-radius: 8px; }
</style>
</head>
<body>
<div class="wrap">
  <div class="nav-row">
    <a class="back" href="../index.html">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="m15 18-6-6 6-6"/></svg>
      AI Lab
    </a>
    @@THEME_CTRL@@
  </div>
  <div data-lab-stack></div>
  <article class="doc">
    <h1>@@TITLE@@</h1>
    <p class="summary">@@SUMMARY@@</p>
    <div class="actions">@@ACTIONS@@</div>
    <div class="topics">@@TOPICS@@</div>
    <hr class="sep" />
    <div class="body">@@BODY@@</div>
  </article>
</div>
<script src="../_shared/nav-stack.js"></script>
<script>
(function () {
  const title = @@TITLE_JS@@;
  const num = @@NUM_JS@@;
  if (window.AiLabNav) {
    AiLabNav.enter((num ? num + " " : "") + title);
    AiLabNav.wireBack("a.back", "../index.html");
  }
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


def _inject_theme(html: str) -> str:
    return (
        html.replace("@@THEME@@", THEME_CSS)
        .replace("@@THEME_BOOT@@", THEME_BOOT)
        .replace("@@LANG_BOOT@@", LANG_BOOT)
        .replace("@@THEME_CTRL@@", PREFS_CTRL)
        .replace("@@PREFS_CTRL@@", PREFS_CTRL)
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
    num_js = json.dumps(n.get("num") or "", ensure_ascii=False)
    return _inject_theme(
        NOTE_HTML.replace("@@TITLE@@", esc(n["title"]))
        .replace("@@SUMMARY@@", esc(n["summary"]))
        .replace("@@ACTIONS@@", "\n".join(actions))
        .replace("@@TOPICS@@", topics)
        .replace("@@BODY@@", n["body_html"])
        .replace("@@TITLE_JS@@", title_js)
        .replace("@@NUM_JS@@", num_js)
    )


def render_hub(payload: dict) -> str:
    data = json.dumps(payload, ensure_ascii=False).replace("<", "\\u003c")
    return _inject_theme(HUB_HTML.replace("@@NOTES_JSON@@", data))


JOURNEY_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>@@TITLE@@ · AI Lab</title>
@@THEME_BOOT@@
@@LANG_BOOT@@
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&family=Sora:wght@400;500;600;700&display=swap" rel="stylesheet" />
<style>
@@THEME@@
.wrap { max-width: 960px; margin: 0 auto; padding: 24px 20px 48px; }
.nav-row { display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
.back { display: inline-flex; align-items: center; gap: 7px; text-decoration: none; color: var(--muted); font: 500 13px var(--mono); }
.back:hover { color: var(--teal); }
.hero { margin: 18px 0 14px; }
.hero .kicker { font: 600 11px var(--mono); letter-spacing: .16em; text-transform: uppercase; color: var(--teal); }
.hero h1 {
  font-family: var(--serif); font-weight: 400; font-size: clamp(32px, 5vw, 44px);
  letter-spacing: -.02em; margin: 6px 0 8px; line-height: 1.1;
}
.hero .lead { color: var(--muted); font-size: 14.5px; line-height: 1.5; max-width: 620px; }
.hero .chain {
  margin-top: 10px; font: 500 12px var(--mono); color: var(--amber);
  letter-spacing: .02em; line-height: 1.5;
}
.moods { display: flex; flex-wrap: wrap; gap: 7px; margin: 0 0 18px; }
.moods button {
  appearance: none; border: 1px solid transparent; background: var(--teal-soft); color: var(--teal);
  border-radius: 999px; padding: 7px 12px; font: 500 12px var(--mono); cursor: pointer;
  transition: border-color .15s, transform .15s, background .15s;
}
.moods button:hover { border-color: var(--teal); }
.moods button.on { background: var(--teal); color: #fff; border-color: var(--teal); }
.map {
  position: relative; display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px;
  margin: 0 0 16px; padding: 4px 0 2px;
}
.map::before {
  content: ""; position: absolute; left: 8%; right: 8%; top: 28px; height: 3px;
  border-radius: 999px;
  background: linear-gradient(90deg, #0f8a9b, #2a9d8f 25%, #c2703a 55%, #d4894a 80%, #3d6b8a);
  opacity: .55; z-index: 0;
}
.map-node {
  position: relative; z-index: 1; appearance: none; border: 1px solid var(--line);
  background: var(--surface); border-radius: 18px; padding: 14px 10px 12px;
  cursor: pointer; text-align: center; color: inherit; box-shadow: var(--shadow);
  transition: transform .18s ease, border-color .18s, box-shadow .18s;
}
.map-node:hover { transform: translateY(-3px); border-color: var(--node); }
.map-node.on {
  border-color: var(--node); transform: translateY(-4px);
  box-shadow: 0 0 0 4px color-mix(in srgb, var(--node) 22%, transparent), var(--shadow);
}
.map-node .n {
  width: 34px; height: 34px; margin: 0 auto 8px; border-radius: 50%;
  display: grid; place-items: center; font: 700 13px var(--mono); color: #fff;
  background: var(--node); box-shadow: 0 0 0 5px color-mix(in srgb, var(--node) 18%, transparent);
}
.map-node .short { font: 700 13px var(--font); letter-spacing: -.01em; }
.map-node .count { margin-top: 4px; font: 500 10px var(--mono); color: var(--muted); }
.map-node[data-tone="1"] { --node: #0f8a9b; }
.map-node[data-tone="2"] { --node: #2a9d8f; }
.map-node[data-tone="3"] { --node: #c2703a; }
.map-node[data-tone="4"] { --node: #d4894a; }
.map-node[data-tone="5"] { --node: #3d6b8a; }
.stage-panel {
  display: none; background: var(--surface); border: 1px solid var(--line);
  border-radius: 22px; padding: 22px 22px 18px; box-shadow: var(--shadow);
  animation: rise .28s ease;
}
.stage-panel.on { display: block; }
@keyframes rise {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
.stage-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
.stage-head .roman { font: 600 12px var(--mono); color: var(--teal); letter-spacing: .1em; }
.stage-head h2 { font-size: 22px; margin: 4px 0 6px; letter-spacing: -.01em; }
.stage-head .goal { color: var(--muted); font-size: 14px; line-height: 1.5; max-width: 640px; }
.stage-nav { display: flex; gap: 6px; }
.stage-nav button {
  appearance: none; border: 1px solid var(--line); background: transparent; color: var(--muted);
  width: 36px; height: 36px; border-radius: 999px; cursor: pointer;
  display: grid; place-items: center; transition: all .15s;
}
.stage-nav button:hover { color: var(--teal); border-color: var(--teal); }
.stops {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 8px; margin-top: 16px;
}
.stop {
  display: flex; flex-direction: column; gap: 4px; text-decoration: none; color: inherit;
  padding: 12px 12px 11px; border-radius: 14px; border: 1px solid var(--line-soft);
  background: linear-gradient(160deg, color-mix(in srgb, var(--teal) 7%, transparent), transparent 70%);
  transition: border-color .15s, transform .15s, background .15s;
  min-height: 96px;
}
.stop:hover { border-color: var(--teal); transform: translateY(-2px); background: var(--teal-soft); }
.stop .meta { display: flex; gap: 8px; align-items: center; }
.stop .num { font: 600 11px var(--mono); color: var(--teal); }
.stop .when { font: 500 11px var(--mono); color: var(--amber); }
.stop .title { font-weight: 600; font-size: 14px; line-height: 1.3; }
.stop .blip { color: var(--muted); font-size: 12.5px; line-height: 1.35; }
.boss {
  margin-top: 14px; padding: 12px 14px; border-left: 3px solid var(--amber);
  background: rgba(194,112,58,.08); border-radius: 0 12px 12px 0;
  font-size: 13.5px; line-height: 1.5; color: var(--ink);
}
.boss strong {
  font: 600 11px var(--mono); letter-spacing: .08em; text-transform: uppercase;
  color: var(--amber); display: block; margin-bottom: 4px;
}
.fin {
  text-align: center; margin: 18px 0 0; padding: 14px 16px;
  color: var(--muted); font: 500 13px var(--mono);
}
.fin a { color: var(--teal); text-decoration: none; }
.fin a:hover { text-decoration: underline; }
@media (max-width: 760px) {
  .map { grid-template-columns: repeat(5, minmax(64px, 1fr)); gap: 6px; overflow-x: auto; }
  .map-node { min-width: 72px; padding: 12px 6px 10px; }
  .map-node .short { font-size: 11px; }
  .stops { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 520px) {
  .stops { grid-template-columns: 1fr; }
  .map::before { top: 24px; }
}
</style>
</head>
<body>
<div class="wrap">
  <div class="nav-row">
    <a class="back" href="./index.html">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="m15 18-6-6 6-6"/></svg>
      AI Lab · notes
    </a>
    @@THEME_CTRL@@
  </div>
  <div data-lab-stack></div>
  <header class="hero">
    <div class="kicker">Map · five stages</div>
    <h1>@@TITLE@@</h1>
    <p class="lead">@@LEAD@@</p>
    <p class="chain">@@TAGLINE@@</p>
  </header>
  <nav class="moods" aria-label="Start by mood">@@MOODS@@</nav>
  <div class="map" role="tablist" aria-label="Journey stages">@@MAP@@</div>
  <div class="panels">@@STAGES@@</div>
  <div class="fin">Back to the <a href="./index.html">hub</a> · search by #topic</div>
</div>
<script src="_shared/nav-stack.js"></script>
<script>
(function () {
  if (window.AiLabNav) {
    AiLabNav.enter("Journey");
    AiLabNav.wireBack("a.back", "./index.html");
  }
  var ids = @@STAGE_IDS@@;
  function show(id) {
    if (ids.indexOf(id) < 0) id = ids[0];
    document.querySelectorAll(".map-node").forEach(function (btn) {
      var on = btn.getAttribute("data-stage") === id;
      btn.classList.toggle("on", on);
      btn.setAttribute("aria-selected", on ? "true" : "false");
    });
    document.querySelectorAll(".stage-panel").forEach(function (panel) {
      panel.classList.toggle("on", panel.id === id);
    });
    document.querySelectorAll(".moods button").forEach(function (btn) {
      btn.classList.toggle("on", btn.getAttribute("data-stage") === id);
    });
    if (location.hash !== "#" + id) {
      history.replaceState(null, "", "#" + id);
    }
  }
  document.querySelectorAll(".map-node, .moods button, [data-go]").forEach(function (el) {
    el.addEventListener("click", function () {
      show(el.getAttribute("data-stage") || el.getAttribute("data-go"));
    });
  });
  window.addEventListener("hashchange", function () {
    show((location.hash || "#").slice(1));
  });
  show((location.hash || "#").slice(1) || ids[0]);
})();
</script>
</body>
</html>
"""


def render_journey(payload: dict) -> str:
    """Build the journey presentation page (not a note)."""
    if not JOURNEY.is_file():
        return ""
    spec = json.loads(JOURNEY.read_text(encoding="utf-8"))
    by_id = {n["id"]: n for n in payload.get("notes") or []}
    stages = spec.get("stages") or []
    stage_ids = [st["id"] for st in stages]

    moods_html = []
    for m in spec.get("moods") or []:
        moods_html.append(
            f'<button type="button" data-stage="{esc(m["stage"])}" title="{esc(m.get("hint") or "")}">'
            f'{esc(m["label"])}</button>'
        )

    map_html = []
    stages_html = []
    for i, st in enumerate(stages, start=1):
        sid = st["id"]
        short = st.get("short") or (st.get("title") or "").split("·")[0].strip() or sid
        notes = [nid for nid in (st.get("notes") or []) if nid in by_id]
        map_html.append(
            f'<button type="button" class="map-node" role="tab" data-stage="{esc(sid)}" '
            f'data-tone="{i}" aria-selected="false">'
            f'<div class="n">{i}</div>'
            f'<div class="short">{esc(short)}</div>'
            f'<div class="count">{len(notes)} notes</div>'
            f"</button>"
        )

        stops = []
        for nid in notes:
            n = by_id[nid]
            blip = (st.get("blips") or {}).get(nid) or n.get("summary") or ""
            href = n.get("page") or f"notes/{nid}.html"
            stops.append(
                f'<a class="stop" href="{esc(href)}">'
                f'<span class="meta"><span class="num">{esc(n.get("num") or "")}</span>'
                f'<span class="when">{esc(n.get("date") or "")}</span></span>'
                f'<span class="title">{esc(n["title"])}</span>'
                f'<span class="blip">{esc(blip)}</span>'
                f"</a>"
            )

        boss = st.get("boss") or ""
        boss_html = (
            f'<div class="boss"><strong>Challenge</strong>{esc(boss)}</div>' if boss else ""
        )
        prev_id = stage_ids[i - 2] if i > 1 else ""
        next_id = stage_ids[i] if i < len(stage_ids) else ""
        nav_btns = []
        if prev_id:
            nav_btns.append(
                f'<button type="button" data-go="{esc(prev_id)}" aria-label="Previous stage">'
                f'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                f'stroke-width="2" stroke-linecap="round"><path d="m15 18-6-6 6-6"/></svg></button>'
            )
        if next_id:
            nav_btns.append(
                f'<button type="button" data-go="{esc(next_id)}" aria-label="Next stage">'
                f'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                f'stroke-width="2" stroke-linecap="round"><path d="m9 18 6-6-6-6"/></svg></button>'
            )
        stages_html.append(
            f'<section class="stage-panel" id="{esc(sid)}" role="tabpanel">'
            f'<div class="stage-head"><div>'
            f'<div class="roman">{esc(st.get("roman") or "")}</div>'
            f'<h2>{esc(st["title"])}</h2>'
            f'<p class="goal">{esc(st.get("goal") or "")}</p>'
            f"</div>"
            f'<div class="stage-nav">{"".join(nav_btns)}</div>'
            f"</div>"
            f'<div class="stops">{"".join(stops)}</div>'
            f"{boss_html}"
            f"</section>"
        )

    title = spec.get("title") or "AI Lab Journey"
    return _inject_theme(
        JOURNEY_HTML.replace("@@TITLE@@", esc(title))
        .replace("@@LEAD@@", esc(spec.get("lead") or ""))
        .replace("@@TAGLINE@@", esc(spec.get("tagline") or ""))
        .replace("@@MOODS@@", "\n".join(moods_html))
        .replace("@@MAP@@", "\n".join(map_html))
        .replace("@@STAGES@@", "\n".join(stages_html))
        .replace("@@STAGE_IDS@@", json.dumps(stage_ids, ensure_ascii=False))
    )


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

    # hub/notes/journey share one nav-stack copy
    shared_src = ROOT / "demos" / "_shared" / "nav-stack.js"
    if shared_src.is_file():
        shared_dst = DOCS / "_shared"
        shared_dst.mkdir(parents=True, exist_ok=True)
        shutil.copy2(shared_src, shared_dst / "nav-stack.js")

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

    journey_html = render_journey(payload)
    if journey_html:
        (DOCS / "journey.html").write_text(journey_html, encoding="utf-8")

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
    print(f"    journey    → {DOCS / 'journey.html'}")
    print(f"    note pages → {NOTES_OUT}/<id>.html")
    print(f"    copied     → docs/demos, docs/slides (+ zip / download.html)")
    print(f"    built_at   {payload['built_at']}")


if __name__ == "__main__":
    main()
