/* Helpers for SEO subpages (breeds, guides, markets).
   Single source of truth for analytics is content/settings.json -> ga4. */

document.getElementById("year") &&
  (document.getElementById("year").textContent = new Date().getFullYear());

function spTrack(event, params) {
  try {
    if (typeof window.gtag === "function") window.gtag("event", event, params || {});
    else (window.dataLayer = window.dataLayer || []).push({ event, ...(params || {}) });
  } catch (_) { /* analytics must never break the page */ }
}

function spInitAnalytics(ga4) {
  if (!ga4) return;
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  const s = document.createElement("script");
  s.async = true;
  s.src = `https://www.googletagmanager.com/gtag/js?id=${ga4}`;
  document.head.appendChild(s);
  window.gtag("js", new Date());
  window.gtag("config", ga4);
}

// Track key conversions on subpages (Reserve / Inquire / WhatsApp links).
document.addEventListener("click", (e) => {
  const a = e.target.closest("a, button");
  if (!a) return;
  const href = (a.getAttribute("href") || "").toLowerCase();
  if (href.includes("wa.me") || href.includes("whatsapp")) spTrack("contact_whatsapp", { method: "whatsapp" });
  else if (href.includes("#inquire") || /reserve|inquire/i.test(a.textContent || "")) spTrack("reserve_click", { location: "subpage" });
}, { capture: true });

// Subpages live one level deep, so settings.json is one folder up.
fetch("../content/settings.json")
  .then((r) => (r.ok ? r.json() : null))
  .then((s) => s && spInitAnalytics(s.ga4))
  .catch(() => {});
