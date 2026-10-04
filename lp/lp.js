// Ad landing pages: point every "Book a call" button at the booking page.
// Set BOOKING_URL once (for example a Cal.com or Calendly link). While it is
// empty, the buttons keep their email fallback, so no page dead-ends.
// UTM and click-id parameters from the ad are passed through to the booking link.
const BOOKING_URL = "";

(() => {
  if (!BOOKING_URL) return;
  let url;
  try { url = new URL(BOOKING_URL); } catch { return; }
  const params = new URLSearchParams(location.search);
  for (const [k, v] of params) {
    if (/^utm_|^(gclid|fbclid)$/.test(k)) url.searchParams.set(k, v);
  }
  url.searchParams.set("utm_content", url.searchParams.get("utm_content") || location.pathname.split("/").filter(Boolean).pop());
  document.querySelectorAll("[data-book]").forEach((a) => { a.href = url.toString(); });
})();
