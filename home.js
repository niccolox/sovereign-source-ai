// Homepage: play the "A Monday, twice" settle-in once when the warehouse column scrolls into view.
// Content is visible by default; this only adds the animation class.
(() => {
  const col = document.querySelector('.monday-yours');
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
