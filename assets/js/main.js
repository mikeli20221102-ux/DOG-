/* =====================================================================
   Pawsport — site logic
   Content (breeds, prices, images, reviews) is loaded from content/*.json
   and edited via Decap CMS at /admin (after GitHub + Netlify setup).
   ===================================================================== */

const CONFIG = {
  email: "Mikeli20221102@gmail.com",
  formEndpoint: "https://formspree.io/f/xbdeaabj",
  whatsapp: "639053191026",
  facebook: "https://www.facebook.com/profile.php?id=100094280424574",
};

let BREEDS = [];
let VIDEOS = [];
let TESTIMONIALS = [];
let SETTINGS = {};

const PLACEHOLDER = "https://placedog.net/600/450?id=";

/* ---------------------- content loading ---------------------- */

async function loadContent() {
  try {
    const [breedsRes, videosRes, testiRes, settingsRes] = await Promise.all([
      fetch("content/breeds.json"),
      fetch("content/videos.json"),
      fetch("content/testimonials.json"),
      fetch("content/settings.json"),
    ]);
    const breeds = await breedsRes.json();
    const videos = await videosRes.json();
    const testi = await testiRes.json();
    const settings = await settingsRes.json();

    BREEDS = (breeds.items || []).filter((b) => b.published !== false);
    VIDEOS = videos.items || [];
    TESTIMONIALS = testi.items || [];
    SETTINGS = settings;

    Object.assign(CONFIG, {
      email: settings.email || CONFIG.email,
      formEndpoint: settings.formEndpoint || CONFIG.formEndpoint,
      whatsapp: settings.whatsapp || CONFIG.whatsapp,
      facebook: settings.facebook || CONFIG.facebook,
    });

    applySettings(settings);
  } catch (err) {
    console.warn("Could not load content/*.json — is the site served over HTTP?", err);
  }
}

function applySettings(s) {
  if (!s) return;
  if (s.stats) {
    const map = [
      ["statFamilies", s.stats.families],
      ["statCountries", s.stats.countries],
      ["statYears", s.stats.years],
      ["statSatisfaction", s.stats.satisfaction],
    ];
    map.forEach(([id, val]) => {
      const el = document.getElementById(id);
      if (el && val) el.textContent = val;
    });
  }
  setImgSrc("aboutImage", s.aboutImage, "https://placedog.net/680/760?id=44");
  setImgSrc("heroImage", s.heroImage, "https://placedog.net/720/820?id=7");
  setImgSrc("deliveryImage", s.deliveryImage, "https://placedog.net/640/720?id=33");
  populateBreedSelect();
}

function setImgSrc(id, src, fallback) {
  const el = document.getElementById(id);
  if (!el || !src) return;
  el.src = src;
  el.onerror = function () { this.onerror = null; this.src = fallback; };
}

function populateBreedSelect() {
  const sel = document.getElementById("breed");
  if (!sel || !BREEDS.length) return;
  const notsure = t("form.notsure");
  sel.innerHTML =
    BREEDS.map((b) => `<option value="${b.name}">${b.name}</option>`).join("") +
    `<option value="Not sure yet">${notsure}</option>`;
}

/* ---------------------- breed helpers ---------------------- */

function normalizeGallery(b, idx) {
  let imgs = [];
  if (Array.isArray(b.gallery) && b.gallery.length) {
    imgs = b.gallery.map((item) =>
      typeof item === "string" ? item : (item.image || item.url || "")
    ).filter(Boolean);
  }
  if (!imgs.length && b.coverImage) imgs = [b.coverImage];
  const base = 110 + idx * 10;
  return imgs.map((img, i) => ({
    img,
    fallback: `${PLACEHOLDER}${base + i + 1}`,
  }));
}

function breedField(b, field) {
  if (currentLang === "zh" && b[field + "_zh"]) return b[field + "_zh"];
  if (b[field + "_en"]) return b[field + "_en"];
  const i18nKey = `breed.${b.key}.${field}`;
  const fromI18n = typeof t === "function" ? t(i18nKey) : "";
  if (fromI18n && fromI18n !== i18nKey) return fromI18n;
  return b[field + "_en"] || "";
}

function priceRange(priceFrom) {
  const low = parseInt(String(priceFrom).replace(/[^0-9]/g, ""), 10) || 0;
  const high = low * 3;
  const fmt = (x) => x.toLocaleString("en-US");
  return `$${fmt(low)} – $${fmt(high)}`;
}

/* ---------------------- render ---------------------- */

function renderBreeds() {
  const grid = document.getElementById("breedGrid");
  if (!grid) return;
  if (!BREEDS.length) {
    grid.innerHTML = `<p class="section-sub">Loading breeds…</p>`;
    return;
  }
  grid.innerHTML = BREEDS.map((b, idx) => {
    const cover = b.coverImage || `assets/img/${b.key}-1.jpg`;
    const fb = `${PLACEHOLDER}${101 + idx}`;
    return `
    <article class="breed-card" data-idx="${idx}">
      <div class="media">
        <span class="tag">${breedField(b, "tag")}</span>
        <img src="${cover}" alt="${b.name} puppy" loading="lazy"
             onerror="this.onerror=null;this.src='${fb}'" />
      </div>
      <div class="body">
        <h3>${b.name}</h3>
        <p class="zh">${b.zh || ""}</p>
        <p class="desc">${breedField(b, "desc")}</p>
        <div class="foot">
          <div class="price">${priceRange(b.priceFrom)}<span>${t("breeds.note")}</span></div>
          <button class="btn btn-small" data-idx="${idx}">${t("breeds.details")}</button>
        </div>
      </div>
    </article>`;
  }).join("");

  grid.querySelectorAll(".breed-card").forEach((card) => {
    card.addEventListener("click", () => openBreedModal(+card.dataset.idx));
  });
}

function openBreedModal(idx) {
  const b = BREEDS[idx];
  const modal = document.getElementById("breedModal");
  const body = document.getElementById("breedModalBody");
  if (!b || !modal || !body) return;

  const gallery = normalizeGallery(b, idx);
  const traitFields = ["size", "temperament", "coat", "lifespan", "goodwith"];
  const mainImg = gallery[0]?.img || b.coverImage;
  const mainFb = gallery[0]?.fallback || PLACEHOLDER + "199";

  body.innerHTML = `
    <div class="bm-gallery">
      <div class="bm-main">
        <img id="bmMain" src="${mainImg}" alt="${b.name}"
             onerror="this.onerror=null;this.src='${mainFb}'" />
      </div>
      <div class="bm-thumbs">
        ${gallery.map((g, i) => `
          <img class="bm-thumb${i === 0 ? " active" : ""}" data-src="${g.img}" data-fb="${g.fallback}"
               src="${g.img}" alt="${b.name} ${i + 1}"
               onerror="this.onerror=null;this.src='${g.fallback}'" />`).join("")}
      </div>
    </div>
    <div class="bm-info">
      <span class="bm-tag">${breedField(b, "tag")}</span>
      <h3>${b.name}</h3>
      <p class="bm-zh">${b.zh || ""}</p>
      <p class="bm-price">${priceRange(b.priceFrom)} · ${t("breeds.note")}</p>
      <h4>${t("detail.about")}</h4>
      <p class="bm-long">${breedField(b, "long")}</p>
      <h4>${t("detail.traits")}</h4>
      <ul class="bm-traits">
        ${traitFields.map((f) => `<li><span>${t("traits." + f)}</span><b>${breedField(b, f)}</b></li>`).join("")}
      </ul>
      <h4>${t("included.title")}</h4>
      <ul class="bm-included">
        ${[1, 2, 3, 4, 5, 6].map((n) => `<li>${t("included.i" + n)}</li>`).join("")}
      </ul>
      <button class="btn btn-block" id="bmInquire">${t("detail.cta")}</button>
    </div>`;

  body.querySelectorAll(".bm-thumb").forEach((th) => {
    th.addEventListener("click", () => {
      const main = document.getElementById("bmMain");
      main.onerror = function () { this.onerror = null; this.src = th.dataset.fb; };
      main.src = th.dataset.src;
      body.querySelectorAll(".bm-thumb").forEach((x) => x.classList.remove("active"));
      th.classList.add("active");
    });
  });

  body.querySelector("#bmInquire").addEventListener("click", () => {
    const sel = document.getElementById("breed");
    if (sel) sel.value = b.name;
    closeBreedModal();
    document.getElementById("inquire").scrollIntoView({ behavior: "smooth" });
  });

  modal.classList.add("open");
  document.body.style.overflow = "hidden";
}

function closeBreedModal() {
  const modal = document.getElementById("breedModal");
  if (!modal) return;
  modal.classList.remove("open");
  document.body.style.overflow = "";
}

function initBreedModal() {
  const modal = document.getElementById("breedModal");
  if (!modal) return;
  modal.addEventListener("click", (e) => {
    if (e.target.hasAttribute("data-close")) closeBreedModal();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeBreedModal();
  });
}

function renderTestimonials() {
  const grid = document.getElementById("testiGrid");
  if (!grid) return;
  grid.innerHTML = TESTIMONIALS.map((r) => {
    const initial = (r.name.trim()[0] || "?").toUpperCase();
    const rating = Math.min(5, Math.max(1, r.rating || 5));
    const stars = "★".repeat(rating) + "☆".repeat(5 - rating);
    return `
      <figure class="testi-card">
        <div class="testi-stars">${stars}</div>
        <blockquote>${r.quote}</blockquote>
        <figcaption>
          <span class="testi-ava">${initial}</span>
          <span class="testi-who"><b>${r.name}</b><small>${r.country}</small></span>
        </figcaption>
      </figure>`;
  }).join("");
}

function renderVideos() {
  const grid = document.getElementById("videoGrid");
  if (!grid) return;
  grid.innerHTML = VIDEOS.map((v, i) => {
    const fb = `https://placedog.net/640/400?id=${201 + i}`;
    return `
    <div class="video-card" data-idx="${i}">
      <img class="poster-img" src="${v.poster}" alt="${v.name}" loading="lazy"
           onerror="this.onerror=null;this.src='${fb}'" />
      <div class="play"><span></span></div>
      <div class="cap">${v.name} · ${v.weeks} ${t("videos.weeks")}</div>
    </div>`;
  }).join("");

  grid.querySelectorAll(".video-card").forEach((card) => {
    card.addEventListener("click", () => {
      const v = VIDEOS[card.dataset.idx];
      if (!v || !v.src) return;
      card.innerHTML = `<video controls autoplay playsinline src="${v.src}"></video>`;
    });
  });
}

function initNav() {
  const toggle = document.getElementById("navToggle");
  const links = document.getElementById("navLinks");
  if (!toggle || !links) return;
  toggle.addEventListener("click", () => links.classList.toggle("open"));
  links.querySelectorAll("a").forEach((a) =>
    a.addEventListener("click", () => links.classList.remove("open"))
  );
}

function initContacts() {
  const wa = CONFIG.whatsapp ? `https://wa.me/${CONFIG.whatsapp}` : "";
  document.querySelectorAll(".js-wa").forEach((a) => {
    if (!wa) return a.remove();
    a.href = wa; a.textContent = "WhatsApp"; a.target = "_blank"; a.rel = "noopener";
  });
  document.querySelectorAll(".js-fb").forEach((a) => {
    if (!CONFIG.facebook) return a.remove();
    a.href = CONFIG.facebook; a.textContent = "Facebook"; a.target = "_blank"; a.rel = "noopener";
  });
  document.querySelectorAll('a[href^="mailto:"]').forEach((a) => {
    a.href = `mailto:${CONFIG.email}`;
    a.textContent = CONFIG.email;
  });
  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();
}

function initForm() {
  const form = document.getElementById("inquiryForm");
  const note = document.getElementById("formNote");
  if (!form) return;

  if (CONFIG.formEndpoint) form.setAttribute("action", CONFIG.formEndpoint);

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    note.className = "form-note";
    note.textContent = "";

    const data = new FormData(form);
    const name = (data.get("name") || "").toString().trim();
    const email = (data.get("email") || "").toString().trim();
    const country = (data.get("country") || "").toString().trim();

    if (!name || !email || !country) {
      note.classList.add("err");
      note.textContent = t("form.errFill");
      return;
    }

    if (!CONFIG.formEndpoint || CONFIG.formEndpoint.includes("your-form-id")) {
      const subject = encodeURIComponent(`Puppy inquiry — ${data.get("breed")}`);
      const body = encodeURIComponent(
        `Name: ${name}\nEmail: ${email}\nWhatsApp/Phone: ${data.get("whatsapp")}\n` +
        `Country/City: ${country}\nBreed: ${data.get("breed")}\n\n${data.get("message")}`
      );
      window.location.href = `mailto:${CONFIG.email}?subject=${subject}&body=${body}`;
      note.classList.add("ok");
      note.textContent = t("form.opening");
      return;
    }

    try {
      const res = await fetch(form.action, {
        method: "POST",
        body: data,
        headers: { Accept: "application/json" },
      });
      if (res.ok) {
        form.reset();
        note.classList.add("ok");
        note.textContent = t("form.thanks");
      } else {
        throw new Error("Request failed");
      }
    } catch (err) {
      note.classList.add("err");
      note.textContent = t("form.error");
    }
  });
}

/* ---------------------- boot ---------------------- */

document.addEventListener("DOMContentLoaded", async () => {
  initI18n();
  await loadContent();
  renderBreeds();
  renderVideos();
  renderTestimonials();
  initBreedModal();
  initNav();
  initContacts();
  initForm();
});

document.addEventListener("langchange", () => {
  renderBreeds();
  renderVideos();
  populateBreedSelect();
});
