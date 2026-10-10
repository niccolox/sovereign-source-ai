// Play a page's one settle-in animation once when its element scrolls into view:
// the homepage's "A Monday, twice" warehouse column, or the rewards pool on llm/.
// Content is visible by default; this only adds the animation class.
(() => {
  const col = document.querySelector('.monday-yours, .pool-tracks-bar');
  if (!col || !('IntersectionObserver' in window)) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const io = new IntersectionObserver((entries) => {
    if (entries.some((e) => e.isIntersecting)) {
      col.classList.add('is-in');
      io.disconnect();
    }
  }, { threshold: 0.35 });
  io.observe(col);
})();
