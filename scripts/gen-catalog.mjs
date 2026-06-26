// Generates a Meta (Facebook/Instagram) + Google product catalog feed for the
// breeds listed in content/breeds.json.
//   Output: meta-catalog.csv  ->  https://silkroadpaws.com/meta-catalog.csv
// Import this URL as a "Scheduled feed" in Meta Commerce Manager, or upload once.
//   Run:  node scripts/gen-catalog.mjs

import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, "..");

const SITE_URL = "https://silkroadpaws.com";
const BRAND = "Pawsport";
// Google product category: Animals & Pet Supplies > Live Animals
const GOOGLE_CATEGORY = "3237";

// breed "key" in breeds.json -> page slug under /breeds/
const SLUG = {
  chow: "chow-chow",
  shihtzu: "shih-tzu",
  crested: "chinese-crested",
  pekingese: "pekingese",
  sharpei: "shar-pei",
  chongqing: "chongqing-dog",
};

const data = JSON.parse(readFileSync(join(root, "content", "breeds.json"), "utf8"));
const items = (data.items || []).filter((b) => b.published !== false);

const headers = [
  "id",
  "title",
  "description",
  "availability",
  "condition",
  "price",
  "link",
  "image_link",
  "brand",
  "product_type",
  "google_product_category",
];

function esc(v) {
  const s = String(v ?? "").replace(/\s+/g, " ").trim();
  return `"${s.replace(/"/g, '""')}"`;
}

function abs(path) {
  if (!path) return "";
  if (/^https?:\/\//.test(path)) return path;
  return `${SITE_URL}/${String(path).replace(/^\/+/, "")}`;
}

const rows = [headers.join(",")];
let count = 0;

for (const b of items) {
  const slug = SLUG[b.key] || b.key;
  if (!slug || !(b.priceFrom > 0)) continue;
  const title = `${b.name} Puppy`.slice(0, 150);
  const desc =
    `${b.desc_en || b.name} ` +
    `Purebred ${b.name} (${b.zh || ""}) from China. ` +
    `Live video viewing, full health & vaccination records, escorted worldwide delivery. From $${b.priceFrom}.`;
  const link = `${SITE_URL}/breeds/${slug}.html`;
  const imageLink = abs(b.coverImage || (b.gallery && b.gallery[0]));

  rows.push(
    [
      esc(b.key || slug),
      esc(title),
      esc(desc),
      esc("in stock"),
      esc("new"),
      esc(`${Number(b.priceFrom).toFixed(2)} USD`),
      esc(link),
      esc(imageLink),
      esc(BRAND),
      esc(`Dog breeds > ${b.name}`),
      esc(GOOGLE_CATEGORY),
    ].join(","),
  );
  count++;
}

const outPath = join(root, "meta-catalog.csv");
writeFileSync(outPath, rows.join("\n"), "utf8");
console.log(`meta-catalog.csv written: ${count} breeds -> ${outPath}`);
