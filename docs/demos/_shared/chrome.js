/* Download + Share chrome for demos (apps) and slides */
(function () {
  const lab = window.LAB || {};
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

  // Both controls are <button> so page-level `a {…}` / mismatched padding cannot skew size.
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
})();
