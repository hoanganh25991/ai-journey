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

  const bar = document.createElement("div");
  bar.className = "lab-chrome";

  if (lab.download) {
    const a = document.createElement("a");
    a.href = lab.download;
    if (lab.downloadName) a.download = lab.downloadName;
    a.textContent = "Download";
    a.setAttribute("aria-label", "Download");
    bar.appendChild(a);
  }

  const shareBtn = document.createElement("button");
  shareBtn.type = "button";
  shareBtn.textContent = "Share";
  shareBtn.addEventListener("click", share);
  bar.appendChild(shareBtn);

  document.body.appendChild(bar);
})();
