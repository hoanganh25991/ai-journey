(function () {
  function scriptDir() {
    const scripts = document.getElementsByTagName("script");
    for (let i = scripts.length - 1; i >= 0; i--) {
      const src = scripts[i].src || "";
      if (src.includes("deck.js")) return src.replace(/[^/]+$/, "");
    }
    return "../_shared/";
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
    const stage = document.getElementById("deckStage");
    const slides = Array.from(document.querySelectorAll(".slide"));
    let index = 0;
    const lab = window.LAB || {};

    // top-left back → previous stack entry (fallback: hub)
    if (!document.querySelector(".deck-home")) {
      const home = document.createElement("a");
      home.className = "deck-home";
      home.href = "../../index.html";
      home.innerHTML =
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg><span>Back</span>';
      document.body.appendChild(home);
    }
    if (window.AiLabNav) {
      const topic =
        (lab.title || document.title || "Slides").replace(/\s*·.*$/, "").trim() || "Slides";
      AiLabNav.enter("Slides · " + topic);
      AiLabNav.wireBack(".deck-home", "../../index.html");
    }

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

    if (!document.querySelector(".lab-chrome")) {
      const bar = document.createElement("div");
      bar.className = "lab-chrome";
      if (lab.download) {
        const dl = document.createElement("button");
        dl.type = "button";
        dl.textContent = "Download";
        dl.setAttribute("aria-label", "Download");
        dl.addEventListener("click", () => {
          const a = document.createElement("a");
          a.href = lab.download;
          if (lab.downloadName) a.download = lab.downloadName;
          a.rel = "noopener";
          document.body.appendChild(a);
          a.click();
          a.remove();
        });
        bar.appendChild(dl);
      }
      const shareBtn = document.createElement("button");
      shareBtn.type = "button";
      shareBtn.textContent = "Share";
      shareBtn.addEventListener("click", share);
      bar.appendChild(shareBtn);
      document.body.appendChild(bar);
    }

    function fit() {
      const s = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
      const x = (window.innerWidth - 1920 * s) / 2;
      const y = (window.innerHeight - 1080 * s) / 2;
      stage.style.transform = `translate(${x}px, ${y}px) scale(${s})`;
    }

    function show(i) {
      index = Math.max(0, Math.min(slides.length - 1, i));
      slides.forEach((slide, n) => {
        const on = n === index;
        slide.classList.toggle("active", on);
        slide.classList.toggle("visible", on);
      });
      const label = document.getElementById("pageLabel");
      if (label) label.textContent = `${index + 1} / ${slides.length}`;
    }

    document.getElementById("nextBtn")?.addEventListener("click", () => show(index + 1));
    document.getElementById("prevBtn")?.addEventListener("click", () => show(index - 1));
    window.addEventListener("keydown", (e) => {
      if (e.key === "ArrowRight" || e.key === " ") {
        e.preventDefault();
        show(index + 1);
      } else if (e.key === "ArrowLeft") {
        e.preventDefault();
        show(index - 1);
      }
    });

    fit();
    show(0);
    window.addEventListener("resize", fit);
  }

  loadNav(boot);
})();
