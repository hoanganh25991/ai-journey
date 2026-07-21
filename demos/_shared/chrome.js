/* Download + Share + Back chrome for demos — mirrors slides/_shared/deck.js */
(function () {
  function scriptDir() {
    const scripts = document.getElementsByTagName("script");
    for (let i = scripts.length - 1; i >= 0; i--) {
      const src = scripts[i].src || "";
      if (src.includes("chrome.js")) {
        return src.replace(/[^/]+$/, "");
      }
    }
    return "../../_shared/";
  }

  function loadNav(then) {
    if (window.AiLabNav) {
      then();
      return;
    }
    const s = document.createElement("script");
    s.src = scriptDir() + "nav-stack.js";
    s.onload = then;
    s.onerror = then;
    document.head.appendChild(s);
  }

  function boot() {
    const lab = window.LAB || {};
    const hubHref = "../../../index.html";

    // top-left Back → previous stack entry (fallback: hub)
    if (!document.querySelector(".demo-home")) {
      const home = document.createElement("a");
      home.className = "demo-home";
      home.href = hubHref;
      home.innerHTML =
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg><span>Back</span>';
      document.body.appendChild(home);
    }

    if (window.AiLabNav) {
      const topic =
        (lab.title || document.title || "Demo").replace(/\s*·.*$/, "").trim() || "Demo";
      AiLabNav.enter("Demo · " + topic);
      AiLabNav.wireBack(".demo-home", hubHref);
      document.querySelectorAll('a[href*="index.html"]').forEach((a) => {
        if (a.classList.contains("demo-home")) return;
        const href = a.getAttribute("href") || "";
        const text = (a.textContent || "").trim().toLowerCase();
        const isHub =
          /(?:\.\.\/)+index\.html$/i.test(href) ||
          text === "lab ui" ||
          text === "home" ||
          text === "ai lab";
        if (isHub) {
          a.addEventListener("click", (e) => {
            if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || a.target === "_blank") return;
            e.preventDefault();
            AiLabNav.goBack(href);
          });
        }
      });
    }

    if (document.querySelector(".lab-chrome")) return;

    function toast(msg) {
      let el = document.querySelector(".lab-toast");
      if (!el) {
        el = document.createElement("div");
        el.className = "lab-toast";
        document.body.appendChild(el);
      }
      el.textContent = msg;
      el.classList.add("on");
      clearTimeout(el._t);
      el._t = setTimeout(() => el.classList.remove("on"), 1600);
    }

    async function share() {
      const title = lab.title || document.title || "AI Lab";
      const url = location.href;
      try {
        if (navigator.share) {
          await navigator.share({ title, url });
          return;
        }
      } catch (e) {
        if (e && e.name === "AbortError") return;
      }
      try {
        await navigator.clipboard.writeText(url);
        toast("Copied link");
      } catch {
        window.prompt("Copy link:", url);
      }
    }

    function download() {
      if (!lab.download) return;
      const a = document.createElement("a");
      a.href = lab.download;
      if (lab.downloadName) a.download = lab.downloadName;
      a.rel = "noopener";
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    const bar = document.createElement("div");
    bar.className = "lab-chrome";

    if (lab.download) {
      const dl = document.createElement("button");
      dl.type = "button";
      dl.className = "lab-chrome-btn";
      dl.textContent = "Download";
      dl.setAttribute("aria-label", "Download");
      dl.addEventListener("click", download);
      bar.appendChild(dl);
    }

    const shareBtn = document.createElement("button");
    shareBtn.type = "button";
    shareBtn.className = "lab-chrome-btn";
    shareBtn.textContent = "Share";
    shareBtn.addEventListener("click", share);
    bar.appendChild(shareBtn);

    document.body.appendChild(bar);
  }

  loadNav(boot);
})();
