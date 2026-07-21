/* AI Lab nav stack — breadcrumb + scroll restore across home → note → slides → demos */
(function (global) {
  const SCROLL_KEY = "ai-lab-scroll";
  const STACK_KEY = "ai-lab-stack";

  function pageKey(href) {
    try {
      const u = new URL(href || location.href, location.href);
      // pathname only — hub ?q= must not fragment the scroll/stack key
      let path = u.pathname.replace(/\/index\.html$/i, "/");
      if (!path.endsWith("/") && !/\.[a-z0-9]+$/i.test(path)) path += "/";
      return path;
    } catch {
      return location.pathname;
    }
  }

  function loadJSON(key, fallback) {
    try {
      const v = JSON.parse(sessionStorage.getItem(key) || "null");
      return v == null ? fallback : v;
    } catch {
      return fallback;
    }
  }
  function saveJSON(key, val) {
    try {
      sessionStorage.setItem(key, JSON.stringify(val));
    } catch (_) {}
  }

  function saveScroll() {
    const map = loadJSON(SCROLL_KEY, {});
    const ent = { y: window.scrollY || window.pageYOffset || 0, t: Date.now() };
    const qEl = document.getElementById("q");
    if (qEl) ent.q = qEl.value || "";
    map[pageKey()] = ent;
    saveJSON(SCROLL_KEY, map);

    // keep stack entry scroll + href in sync
    const stack = loadJSON(STACK_KEY, []);
    const key = pageKey();
    for (let i = stack.length - 1; i >= 0; i--) {
      if (stack[i].key === key) {
        stack[i].scroll = ent.y;
        stack[i].href = location.href.split("#")[0];
        if (ent.q != null) stack[i].q = ent.q;
        saveJSON(STACK_KEY, stack);
        break;
      }
    }
  }

  function restoreScroll() {
    const map = loadJSON(SCROLL_KEY, {});
    const ent = map[pageKey()];
    if (!ent) return;
    const y = typeof ent === "number" ? ent : ent.y;
    const q = typeof ent === "object" ? ent.q : undefined;
    const qEl = document.getElementById("q");
    if (qEl && q != null) {
      const params = new URLSearchParams(location.search);
      if (qEl.value !== q) {
        qEl.value = q;
        qEl.dispatchEvent(new Event("input", { bubbles: true }));
      } else if (!params.get("q") && q) {
        // keep URL in sync when returning via stack without ?q=
        qEl.dispatchEvent(new Event("input", { bubbles: true }));
      }
    }
    const apply = () => window.scrollTo(0, y || 0);
    requestAnimationFrame(() => {
      apply();
      setTimeout(apply, 0);
      setTimeout(apply, 40);
      setTimeout(apply, 120);
    });
  }

  function enter(label) {
    const key = pageKey();
    const href = location.href.split("#")[0];
    let stack = loadJSON(STACK_KEY, []);
    const idx = stack.findIndex((e) => e.key === key);
    if (idx >= 0) {
      stack = stack.slice(0, idx + 1);
      stack[idx].label = label || stack[idx].label;
      stack[idx].href = href;
    } else {
      stack.push({ key, href, label: label || document.title || "Page" });
    }
    saveJSON(STACK_KEY, stack);
    renderCrumb(stack);
    restoreScroll();
  }

  function goToStackIndex(i) {
    const stack = loadJSON(STACK_KEY, []);
    if (i < 0 || i >= stack.length) return;
    saveScroll();
    const target = stack[i];
    saveJSON(STACK_KEY, stack.slice(0, i + 1));
    if (pageKey(target.href) === pageKey()) {
      restoreScroll();
      renderCrumb(loadJSON(STACK_KEY, []));
      return;
    }
    location.href = target.href;
  }

  function goBack(fallbackHref) {
    const stack = loadJSON(STACK_KEY, []);
    const key = pageKey();
    const idx = stack.findIndex((e) => e.key === key);
    if (idx > 0) {
      goToStackIndex(idx - 1);
      return;
    }
    if (fallbackHref) location.href = fallbackHref;
    else if (history.length > 1) history.back();
  }

  function ensureCrumbHost() {
    let host = document.getElementById("labStack");
    if (host) return host;
    host = document.createElement("nav");
    host.id = "labStack";
    host.className = "lab-stack";
    host.setAttribute("aria-label", "Navigation stack");

    // Prefer known slots; else insert near top
    const slot =
      document.querySelector("[data-lab-stack]") ||
      document.querySelector(".nav-row") ||
      document.querySelector("header") ||
      document.body;
    if (slot === document.body) {
      host.classList.add("lab-stack-float");
      document.body.appendChild(host);
    } else if (slot.classList && slot.classList.contains("nav-row")) {
      host.classList.add("lab-stack-row");
      slot.insertAdjacentElement("afterend", host);
    } else if (slot.tagName === "HEADER") {
      slot.appendChild(host);
    } else {
      slot.appendChild(host);
    }
    return host;
  }

  function renderCrumb(stack) {
    if (!stack || stack.length < 2) {
      const existing = document.getElementById("labStack");
      if (existing) existing.hidden = true;
      return;
    }
    const host = ensureCrumbHost();
    host.hidden = false;
    host.innerHTML = stack
      .map((e, i) => {
        const last = i === stack.length - 1;
        const label = escapeHtml(e.label || "Page");
        if (last) return `<span class="here">${label}</span>`;
        return `<a href="${escapeHtml(e.href)}" data-stack-i="${i}">${label}</a><span class="sep">›</span>`;
      })
      .join("");
  }

  function escapeHtml(s) {
    return String(s ?? "").replace(/[&<>"']/g, (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])
    );
  }

  function wireBack(selector, fallbackHref) {
    document.querySelectorAll(selector).forEach((a) => {
      a.addEventListener("click", (e) => {
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || a.target === "_blank") return;
        e.preventDefault();
        goBack(fallbackHref || a.getAttribute("href"));
      });
    });
  }

  // Save scroll before leaving via in-lab links
  document.addEventListener(
    "click",
    (e) => {
      const a = e.target.closest && e.target.closest("a[href]");
      if (!a || a.hasAttribute("download")) return;
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || a.target === "_blank") return;
      if (a.hasAttribute("data-stack-i")) {
        e.preventDefault();
        goToStackIndex(Number(a.getAttribute("data-stack-i")));
        return;
      }
      let url;
      try {
        url = new URL(a.href, location.href);
      } catch {
        return;
      }
      if (url.protocol === "mailto:" || url.protocol === "javascript:") return;
      // same document hash only
      if (url.pathname === location.pathname && url.search === location.search && url.hash) return;
      saveScroll();
    },
    true
  );

  if ("scrollRestoration" in history) history.scrollRestoration = "manual";
  window.addEventListener("pagehide", saveScroll);
  window.addEventListener("pageshow", () => restoreScroll());

  // Minimal CSS once
  if (!document.getElementById("labStackStyle")) {
    const style = document.createElement("style");
    style.id = "labStackStyle";
    style.textContent = `
.lab-stack {
  display: flex; flex-wrap: wrap; align-items: center; gap: 2px 0;
  font: 500 12px "IBM Plex Mono", ui-monospace, monospace;
  color: var(--muted, #5a6b80); margin: 10px 0 0; line-height: 1.4;
}
.lab-stack a { color: var(--teal, #0f8a9b); text-decoration: none; }
.lab-stack a:hover { text-decoration: underline; }
.lab-stack .sep { opacity: .45; margin: 0 7px; user-select: none; }
.lab-stack .here { color: var(--ink, #16202e); }
.lab-stack-float {
  position: fixed; left: 14px; bottom: 14px; z-index: 40;
  margin: 0; padding: 8px 12px; border-radius: 999px;
  background: rgba(255,255,255,.92); border: 1px solid rgba(20,32,46,.12);
  box-shadow: 0 1px 2px rgba(20,32,46,.05), 0 8px 24px rgba(20,32,46,.06);
  max-width: min(92vw, 520px);
}
.lab-stack-row { margin: 8px 0 0; }
`;
    document.head.appendChild(style);
  }

  global.AiLabNav = {
    enter,
    saveScroll,
    restoreScroll,
    goBack,
    wireBack,
    pageKey,
  };
})(window);
