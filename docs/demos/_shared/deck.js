(function () {
  const stage = document.getElementById("deckStage");
  const slides = Array.from(document.querySelectorAll(".slide"));
  let index = 0;

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
})();
