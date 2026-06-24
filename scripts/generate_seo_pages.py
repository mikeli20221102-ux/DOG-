#!/usr/bin/env python3
"""Generate static SEO pages (breeds, guides, markets) for Pawsport."""
from __future__ import annotations

import json
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://silkroadpaws.com"

BREEDS = [
    {
        "slug": "chow-chow",
        "key": "chow",
        "name": "Chow Chow",
        "zh": "松狮",
        "price": 1500,
        "title": "Chow Chow Puppies for Sale — Import from China | Pawsport",
        "desc": "Reserve a Chow Chow puppy from China. Lion-maned, vet-checked, microchipped. Live video viewing, full export papers, escorted delivery to Korea, Middle East & more. From $1,500.",
        "kw": "chow chow for sale, chow chow price, chow chow puppies, buy chow chow",
        "tag": "Iconic · Best seller",
        "img": "chow-1.jpg",
        "intro": "The Chow Chow is one of China's most iconic breeds — lion-like mane, blue-black tongue, dignified temperament. Highly sought in the Middle East, Philippines and Russia.",
        "body": """
<p>Our Chow Chow puppies are raised at a professional breeding base in China with 12+ years of experience. Every puppy is vet-checked, vaccinated and microchipped before export.</p>
<h2>Why buyers choose Chow Chow from China</h2>
<ul>
<li><strong>Distinctive appearance</strong> — thick coat, regal stance, instantly recognizable</li>
<li><strong>Strong demand</strong> in UAE, Saudi Arabia, Philippines and Russia</li>
<li><strong>Full compliance</strong> — ISO microchip, rabies vaccination, antibody titer test, health certificate</li>
<li><strong>Live video</strong> — meet your actual puppy before you reserve</li>
</ul>
<h2>Typical price range</h2>
<p>Our Chow Chow puppies start from <strong>$1,500</strong> (breed price only; international escort delivery quoted separately by destination). Local retail in the Middle East often runs $3,000–7,500 including delivery.</p>
<h2>Delivery timeline</h2>
<p>Export compliance (chip, rabies vaccine, titer test, permits) typically takes <strong>2–4 months</strong> depending on your country. We confirm feasibility before you reserve.</p>
""",
    },
    {
        "slug": "shih-tzu",
        "key": "shihtzu",
        "name": "Shih Tzu",
        "zh": "西施",
        "price": 900,
        "title": "Shih Tzu Puppies for Sale — China Export to Korea & Asia | Pawsport",
        "desc": "Shih Tzu puppies from China — gentle, apartment-friendly companions. Live video, health docs, escorted delivery to Korea, Japan, Philippines & Southeast Asia. From $900.",
        "kw": "shih tzu puppies for sale, shih tzu price, shih tzu breeders",
        "tag": "Companion · Apartment-friendly",
        "img": "shihtzu-1.jpg",
        "intro": "The Shih Tzu is a sweet, sociable small breed perfect for apartment life — especially popular in Korea, Japan and Southeast Asia.",
        "body": """
<p>Shih Tzu puppies from our Chinese kennel come with vaccinations, microchip, pedigree documentation and a health guarantee in the sales contract.</p>
<h2>Perfect for urban families</h2>
<ul>
<li>Small size (4–7 kg) — ideal for apartments</li>
<li>Gentle with children, adaptable and affectionate</li>
<li>High search demand in Korea (시츄) and Japan (シーズー)</li>
<li>Full export paperwork handled by our team</li>
</ul>
<h2>Price & delivery</h2>
<p>From <strong>$900</strong> (breed price; delivery quoted by country). Korea and Philippines are among our most efficient markets for small breeds.</p>
""",
    },
    {
        "slug": "chinese-crested",
        "key": "crested",
        "name": "Chinese Crested",
        "zh": "冠毛犬",
        "price": 1200,
        "title": "Chinese Crested Puppies for Sale — Rare & Cabin-Friendly | Pawsport",
        "desc": "Chinese Crested puppies from China — rare, low-shedding, cabin-friendly. Live video viewing, full health records, worldwide escorted delivery. From $1,200.",
        "kw": "chinese crested for sale, chinese crested dog price, chinese crested puppies",
        "tag": "Rare · Cabin-friendly",
        "img": "crested-1.jpg",
        "intro": "The Chinese Crested is elegant, rare and small enough for in-cabin travel — our easiest breed to deliver worldwide.",
        "body": """
<p>Chinese Crested dogs are among the rarest companion breeds we export. Hairless or powderpuff varieties available from our breeding base.</p>
<h2>Why Chinese Crested stands out</h2>
<ul>
<li><strong>Low shedding</strong> — popular with allergy-conscious owners</li>
<li><strong>Small & portable</strong> — can travel in-cabin on many routes</li>
<li><strong>High demand</strong> in Korea and Japan (チャイニーズ・クレステッド)</li>
<li>Rare Chinese bloodline — strong differentiation vs local Maltese or Poodle markets</li>
</ul>
<h2>Price</h2>
<p>From <strong>$1,200</strong>. Premium pricing supported by rarity and cabin-friendly delivery options.</p>
""",
    },
    {
        "slug": "pekingese",
        "key": "pekingese",
        "name": "Pekingese",
        "zh": "京巴",
        "price": 1000,
        "title": "Pekingese Puppies for Sale — Imperial Chinese Breed | Pawsport",
        "desc": "Pekingese (Beijing Dog) puppies from China. Compact imperial lapdog with full health docs. Export to Japan, Korea & worldwide. From $1,000.",
        "kw": "pekingese puppies for sale, pekingese price, pekingese breeder",
        "tag": "Imperial · Small breed",
        "img": "pekingese-1.jpg",
        "intro": "The Pekingese was bred for Chinese royalty — compact, affectionate and full of character. Especially popular in Japan (ペキニーズ).",
        "body": """
<p>Our Pekingese puppies are raised for health and temperament, with full vaccination and microchip before export.</p>
<h2>Breed highlights</h2>
<ul>
<li>Small (3–6 kg) — perfect indoor companion</li>
<li>Strong cultural connection in Japan</li>
<li>Long flowing coat, regal personality</li>
<li>Note: Japan requires 180-day wait after rabies titer — we plan timelines upfront</li>
</ul>
<p>From <strong>$1,000</strong>. <a href="../guide/import-dogs-japan.html">Read our Japan import guide →</a></p>
""",
    },
    {
        "slug": "shar-pei",
        "key": "sharpei",
        "name": "Shar-Pei",
        "zh": "沙皮",
        "price": 900,
        "title": "Shar-Pei Puppies for Sale — Import from China | Pawsport",
        "desc": "Shar-Pei puppies from China — distinctive wrinkles, loyal guardian. Vet-checked, export-ready, escorted delivery to Middle East & Russia. From $900.",
        "kw": "shar pei puppies for sale, shar pei price, chinese shar pei",
        "tag": "Distinctive · Guardian",
        "img": "sharpei-1.jpg",
        "intro": "The Shar-Pei is instantly recognizable — deep wrinkles, loyal and protective. Strong demand in the Middle East and Russia.",
        "body": """
<p>Shar-Pei from our kennel are health-tested, socialized and prepared for international relocation with full export documentation.</p>
<ul>
<li>Unique appearance — high recognition value</li>
<li>Calm, loyal temperament</li>
<li>Popular in UAE, Saudi Arabia and Russia</li>
</ul>
<p>From <strong>$900</strong>.</p>
""",
    },
    {
        "slug": "chongqing-dog",
        "key": "chongqing",
        "name": "Chongqing Dog",
        "zh": "重庆犬",
        "price": 1800,
        "title": "Chongqing Dog for Sale — Rare Chinese Breed | Pawsport",
        "desc": "Extremely rare Chongqing Dog from China — ancient athletic breed for collectors. Full export compliance, escorted delivery. From $1,800.",
        "kw": "chongqing dog, rare chinese dog breed, chinese dog collector",
        "tag": "Very rare · Collector",
        "img": "chongqing-1.jpg",
        "intro": "The Chongqing Dog is an ancient, athletic Chinese breed seldom seen outside China — a prize for serious collectors.",
        "body": """
<p>We export very few Chongqing Dogs each year. This breed is ideal for collectors in Russia and the Middle East seeking something truly unique.</p>
<ul>
<li>Extremely rare outside China</li>
<li>Athletic, brave, intensely loyal</li>
<li>Collector-grade pricing supported by scarcity</li>
</ul>
<p>From <strong>$1,800</strong> — premium collector pricing.</p>
""",
    },
]

GUIDES = [
    {
        "slug": "import-dogs-korea",
        "title": "How to Import a Dog from China to South Korea (2026 Guide)",
        "desc": "Step-by-step guide: importing a puppy from China to Korea — microchip, rabies titer, quarantine rules, timeline and costs. Pawsport handles full compliance.",
        "eyebrow": "Import guide",
        "body": """
<p>South Korea is one of the <strong>easiest markets</strong> for importing dogs from China — especially small breeds like Shih Tzu, Chinese Crested and Pekingese that Korean apartment owners love.</p>
<h2>Requirements for importing a dog to Korea</h2>
<ol>
<li><strong>ISO microchip</strong> — implanted before rabies vaccination</li>
<li><strong>Rabies vaccination</strong> — valid, administered after microchip</li>
<li><strong>Rabies antibody titer test (RNATT)</strong> — ≥0.5 IU/mL from an approved lab</li>
<li><strong>Health certificate</strong> — issued by official veterinarian within 10 days of travel</li>
<li><strong>Import permit</strong> — destination country approval</li>
</ol>
<h2>Timeline</h2>
<p>After the titer blood sample is taken, Korea may allow entry once results pass — often faster than Japan. Total preparation typically <strong>2–3 months</strong> if started promptly.</p>
<h2>Best breeds for Korea</h2>
<p>Chinese Crested, Shih Tzu and Pekingese are top sellers — small, apartment-friendly, and differentiated from local Maltese/Poodle markets.</p>
<h2>What Pawsport handles</h2>
<ul>
<li>Live video viewing before you reserve</li>
<li>All export paperwork from China</li>
<li>Professional flight-nanny escort to your city</li>
<li>No online card payment — deposit by bank transfer + signed contract</li>
</ul>
""",
    },
    {
        "slug": "import-dogs-japan",
        "title": "Importing a Dog from China to Japan — 180-Day Rule Explained",
        "desc": "Complete guide to bringing a puppy from China to Japan: microchip, rabies titer, mandatory 180-day waiting period, health certificate and delivery options.",
        "eyebrow": "Import guide",
        "body": """
<p>Japan welcomes small Chinese breeds — Shih Tzu (シーズー), Pekingese (ペキニーズ) and Chinese Crested are especially popular. The main challenge is <strong>time</strong>: Japan requires a 180-day wait after rabies antibody testing.</p>
<h2>Japan import steps</h2>
<ol>
<li>ISO microchip before rabies vaccine</li>
<li>Rabies vaccination (2 doses as required)</li>
<li>Rabies antibody titer test at approved laboratory</li>
<li><strong>Wait 180 days</strong> from the date blood was drawn (if titer passes)</li>
<li>Advance notification to Animal Quarantine Service (AQS)</li>
<li>Health certificate within 10 days of departure</li>
<li>Inspection on arrival at designated airport</li>
</ol>
<h2>Plan ahead</h2>
<p>Start at least <strong>7 months before</strong> your desired arrival date. We help buyers understand the timeline before they reserve — no surprises.</p>
<h2>Why Japan buyers choose Chinese breeds</h2>
<p>Pekingese has historical ties to Japan (狆). Shih Tzu ranks among popular small breeds. Chinese bloodlines offer rarity and quality differentiation.</p>
""",
    },
    {
        "slug": "import-dogs-middle-east",
        "title": "Importing Dogs from China to UAE & Saudi Arabia",
        "desc": "How to import Chow Chow, Shar-Pei and rare Chinese breeds to the Middle East. Health certs, permits, escorted delivery and typical pricing.",
        "eyebrow": "Import guide",
        "body": """
<p>The Middle East (UAE, Saudi Arabia, Qatar) is our <strong>highest-margin market</strong> for premium Chinese breeds — especially Chow Chow, Shar-Pei and Chongqing Dog.</p>
<h2>Why Middle East buyers import from China</h2>
<ul>
<li>Rare breeds with strong social status value</li>
<li>Retail prices often $3,000–7,500 including delivery</li>
<li>Chinese kennels offer competitive source pricing</li>
</ul>
<h2>Typical requirements</h2>
<ol>
<li>ISO microchip + rabies vaccination</li>
<li>Rabies titer test (≥0.5 IU/mL)</li>
<li>Import permit from destination authority</li>
<li>Veterinary health certificate</li>
<li>Escorted air cargo or flight-nanny delivery</li>
</ol>
<h2>Top breeds for Middle East</h2>
<p><strong>Chow Chow</strong> leads demand — lion mane, iconic look. Shar-Pei and Chinese Crested also perform well for buyers seeking distinction.</p>
""",
    },
    {
        "slug": "how-china-dog-export-works",
        "title": "How Buying a Puppy from China Works — 5-Step Process",
        "desc": "From live video call to door delivery: how Pawsport exports Chinese dog breeds worldwide. Health checks, compliance, escort delivery explained.",
        "eyebrow": "Process",
        "body": """
<h2>Step 1 — Browse & video call</h2>
<p>Explore our breeds online and schedule a <strong>live video call</strong> to meet your actual puppy. No stock photos — you see the real dog.</p>
<h2>Step 2 — Health & pedigree review</h2>
<p>We share vet check results, vaccination records, microchip number and pedigree documents.</p>
<h2>Step 3 — Reserve offline</h2>
<p>Secure your puppy with a deposit via <strong>bank transfer and signed contract</strong>. We never take card payments on this website.</p>
<h2>Step 4 — Export compliance</h2>
<p>We prepare microchip, rabies titer, health certificate and import permits for your country. Timeline: typically 2–4 months (Japan: ~7 months).</p>
<h2>Step 5 — White-glove delivery</h2>
<p>A professional pet escort accompanies your puppy and hand-delivers to your city. Balance paid on safe arrival.</p>
""",
    },
    {
        "slug": "chow-chow-buyers-guide",
        "title": "Chow Chow Price Guide — What to Expect When Importing",
        "desc": "Chow Chow puppy prices from China vs Middle East retail. What's included, delivery costs, and how to avoid scams when importing a Chow Chow.",
        "eyebrow": "Breed guide",
        "body": """
<h2>Chow Chow price ranges</h2>
<table class="data-table">
<tr><th>Market</th><th>Typical retail (USD)</th><th>Our starting price</th></tr>
<tr><td>Middle East (UAE/SA)</td><td>$3,000 – $7,500</td><td>From $1,500 + delivery</td></tr>
<tr><td>Philippines</td><td>$860 – $3,450</td><td>From $1,500 + delivery</td></tr>
<tr><td>Russia</td><td>$1,000 – $2,500</td><td>From $1,500 + delivery</td></tr>
</table>
<p>Our price is the <strong>breed price from China</strong>. International escort delivery is quoted separately based on your city — buyers typically pay delivery as a pass-through cost.</p>
<h2>What's included</h2>
<ul>
<li>Vet check, vaccinations, microchip</li>
<li>Pedigree & health documentation</li>
<li>Export paperwork from China</li>
<li>Live video viewing before reserve</li>
</ul>
<h2>Red flags to avoid</h2>
<ul>
<li>Sellers who won't do live video</li>
<li>Online card payment with no contract</li>
<li>Prices that seem too good to be true</li>
<li>No mention of titer test or import permits</li>
</ul>
""",
    },
    {
        "slug": "chinese-crested-apartment-dogs",
        "title": "Chinese Crested — Best Rare Apartment Dog for Korea & Japan",
        "desc": "Why Chinese Crested is ideal for apartment living: low shedding, small size, cabin travel. Import from China with Pawsport.",
        "eyebrow": "Breed guide",
        "body": """
<p>Korean and Japanese urban buyers increasingly search for <strong>small, low-shedding, rare breeds</strong> — Chinese Crested (冠毛犬 / 채니즈 크레스티드 / チャイクレ) fits perfectly.</p>
<h2>Apartment advantages</h2>
<ul>
<li>Weight only 4–5 kg</li>
<li>Hairless or powderpuff — minimal shedding</li>
<li>Quiet, devoted companion</li>
<li>Often eligible for in-cabin flight (route-dependent)</li>
</ul>
<h2>Search demand</h2>
<p>Japanese searches for チャイニーズ・クレステッド・ドッグ and Korean interest in 채니즈 크레스티드 continue to grow — a differentiated alternative to Maltese and Poodle.</p>
<p><a href="../breeds/chinese-crested.html">View Chinese Crested puppies →</a></p>
""",
    },
]

MARKETS = [
    {
        "slug": "korea",
        "title": "Import Chinese Dog Breeds to Korea — Pawsport",
        "desc": "Shih Tzu, Chinese Crested & Pekingese to Seoul and Korea. Live video, full docs, escorted delivery. 시츄 · 차우차우 · 크레스티드.",
        "h1": "Chinese dog breeds for Korea",
        "lead": "Small, rare Chinese breeds for Korean apartment life — with live video viewing and full import compliance.",
        "breeds": ["chinese-crested", "shih-tzu", "pekingese", "chow-chow"],
        "guide": "import-dogs-korea",
    },
    {
        "slug": "japan",
        "title": "Import Chinese Dog Breeds to Japan — Pawsport",
        "desc": "Pekingese, Shih Tzu & Chinese Crested to Japan. ペキニーズ · シーズー · チャウチャウ. Full 180-day compliance handled.",
        "h1": "Chinese dog breeds for Japan",
        "lead": "Heritage breeds with strong Japanese appeal — we manage the 180-day import timeline from day one.",
        "breeds": ["pekingese", "shih-tzu", "chinese-crested", "chow-chow"],
        "guide": "import-dogs-japan",
    },
    {
        "slug": "philippines",
        "title": "Import Chow Chow & Shih Tzu to Philippines — Pawsport",
        "desc": "Chow Chow and Shih Tzu puppies from China to the Philippines. Facebook-friendly breeds, escorted delivery, full paperwork.",
        "h1": "Chinese dog breeds for the Philippines",
        "lead": "Chow Chow for premium buyers, Shih Tzu for volume — social-media ready puppies with full export docs.",
        "breeds": ["chow-chow", "shih-tzu", "pekingese"],
        "guide": "how-china-dog-export-works",
    },
]


def rel(depth: int) -> str:
    return "../" * depth if depth else "./"


def shell(title: str, desc: str, path: str, body: str, depth: int = 1, extra_head: str = "", json_ld: str = "") -> str:
    canonical = f"{SITE}{path}"
    r = rel(depth)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="site-url" content="{SITE}/" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:site_name" content="Pawsport" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{r}assets/css/styles.css" />
  {extra_head}
  {json_ld}
</head>
<body class="subpage">
  <header class="site-header">
    <div class="container nav">
      <a class="brand" href="{r}index.html"><span class="brand-mark">Paws<span>port</span></span></a>
      <nav class="nav-links">
        <a href="{r}index.html#breeds">Breeds</a>
        <a href="{r}guide/index.html">Guides</a>
        <a href="{r}index.html#inquire" class="btn btn-small">Reserve</a>
      </nav>
    </div>
  </header>
  <main>
    {body}
  </main>
  <footer class="site-footer">
    <div class="container footer-bottom">
      <p>© Pawsport · <a href="{r}index.html">Home</a> · <a href="{r}guide/index.html">Guides</a></p>
    </div>
  </footer>
  <script src="{r}assets/js/subpage.js"></script>
</body>
</html>"""


def depth_prefix(depth: int) -> str:
    return "../" * depth if depth else ""


def article_wrap(eyebrow: str, h1: str, lead: str, content: str, cta_breed: str | None = None) -> str:
    cta = ""
    if cta_breed:
        cta = f'<p class="article-cta"><a class="btn" href="../index.html#inquire">Inquire about {cta_breed}</a></p>'
    return f"""
    <article class="article-page">
      <div class="container narrow">
        <nav class="breadcrumb" aria-label="Breadcrumb">
          <a href="../index.html">Home</a> <span>/</span> <a href="index.html">Guides</a>
        </nav>
        <p class="eyebrow">{eyebrow}</p>
        <h1>{h1}</h1>
        <p class="lead">{lead}</p>
        <div class="prose">{content}</div>
        {cta}
      </div>
    </article>"""


def breed_page(b: dict) -> str:
    path = f"/breeds/{b['slug']}.html"
    prefix = "../"
    json_ld = f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Product","name":"{b['name']} Puppy","description":"{b['desc'][:200]}","brand":{{"@type":"Brand","name":"Pawsport"}},"offers":{{"@type":"Offer","priceCurrency":"USD","price":"{b['price']}","availability":"https://schema.org/InStock","url":"{SITE}{path}"}}}}
</script>"""
    body = f"""
    <article class="article-page">
      <div class="container">
        <nav class="breadcrumb"><a href="{prefix}index.html">Home</a> <span>/</span> <span>{b['name']}</span></nav>
        <div class="breed-hero">
          <div class="breed-hero-copy">
            <p class="eyebrow">{b['tag']}</p>
            <h1>{b['name']} Puppies for Sale</h1>
            <p class="lead">{b['intro']}</p>
            <p class="price-line">From <strong>${b['price']:,}</strong> <span>(breed price · delivery quoted separately)</span></p>
            <a class="btn" href="{prefix}index.html#inquire">Reserve / Inquire</a>
          </div>
          <div class="breed-hero-img">
            <img src="{prefix}assets/img/{b['img']}" alt="{b['name']} puppy" loading="eager"
                 onerror="this.onerror=null;this.src='https://placedog.net/720/540?id=12'" />
          </div>
        </div>
        <div class="prose container narrow">{b['body']}</div>
        <p class="article-cta center"><a class="btn" href="{prefix}index.html#inquire">Inquire about {b['name']}</a></p>
      </div>
    </article>"""
    return shell(b["title"], b["desc"], path, body, 1, f'<meta name="keywords" content="{b["kw"]}" />', json_ld)


def guide_page(g: dict) -> str:
    path = f"/guide/{g['slug']}.html"
    h1 = g["title"].split("—")[0].strip() if "—" in g["title"] else g["title"]
    body = article_wrap(g["eyebrow"], h1, g["desc"][:160], g["body"])
    json_ld = f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":"{g['title']}","description":"{g['desc'][:200]}","author":{{"@type":"Organization","name":"Pawsport"}},"publisher":{{"@type":"Organization","name":"Pawsport"}}}}
</script>"""
    return shell(g["title"], g["desc"], path, body, 1, "", json_ld)


def market_page(m: dict) -> str:
    path = f"/markets/{m['slug']}.html"
    breed_links = "\n".join(
        f'<li><a href="../breeds/{s}.html">{s.replace("-", " ").title()}</a></li>' for s in m["breeds"]
    )
    content = f"""
    <p>We deliver to major cities in this market with full export compliance from China.</p>
    <h2>Popular breeds</h2>
    <ul>{breed_links}</ul>
    <p><a href="../guide/{m['guide']}.html">Read the import guide for this market →</a></p>
    """
    body = article_wrap("Market", m["h1"], m["lead"], content)
    return shell(m["title"], m["desc"], path, body, 1)


def guide_index() -> str:
    links = "\n".join(
        f'<li><a href="{g["slug"]}.html"><strong>{g["title"].split("—")[0].strip()}</strong><span>{g["desc"][:100]}…</span></a></li>'
        for g in GUIDES
    )
    breed_links = "\n".join(
        f'<li><a href="../breeds/{b["slug"]}.html">{b["name"]}</a></li>' for b in BREEDS
    )
    body = f"""
    <article class="article-page">
      <div class="container narrow">
        <nav class="breadcrumb"><a href="../index.html">Home</a> <span>/</span> <span>Guides</span></nav>
        <p class="eyebrow">Knowledge base</p>
        <h1>Dog import & breed guides</h1>
        <p class="lead">Practical guides for importing Chinese dog breeds — compliance, timelines and breed tips.</p>
        <h2>Import guides</h2>
        <ul class="guide-list">{links}</ul>
        <h2>Breed pages</h2>
        <ul class="guide-list">{breed_links}</ul>
      </div>
    </article>"""
    return shell(
        "Dog Import Guides & Breed Resources | Pawsport",
        "Guides for importing Chinese dog breeds to Korea, Japan, Middle East and more. Chow Chow, Shih Tzu, Chinese Crested.",
        "/guide/index.html",
        body,
        1,
    )


def sitemap(urls: list[str]) -> str:
    items = "\n".join(
        f"  <url><loc>{SITE}{u}</loc><changefreq>weekly</changefreq><priority>{'0.9' if u == '/' else '0.7'}</priority></url>"
        for u in urls
    )
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}\n</urlset>\n'


def main():
    (ROOT / "breeds").mkdir(exist_ok=True)
    (ROOT / "guide").mkdir(exist_ok=True)
    (ROOT / "markets").mkdir(exist_ok=True)

    urls = ["/", "/guide/index.html"]

    for b in BREEDS:
        p = ROOT / "breeds" / f"{b['slug']}.html"
        p.write_text(breed_page(b), encoding="utf-8")
        urls.append(f"/breeds/{b['slug']}.html")
        print(f"  breeds/{b['slug']}.html")

    (ROOT / "guide" / "index.html").write_text(guide_index(), encoding="utf-8")
    for g in GUIDES:
        p = ROOT / "guide" / f"{g['slug']}.html"
        p.write_text(guide_page(g), encoding="utf-8")
        urls.append(f"/guide/{g['slug']}.html")
        print(f"  guide/{g['slug']}.html")

    for m in MARKETS:
        p = ROOT / "markets" / f"{m['slug']}.html"
        p.write_text(market_page(m), encoding="utf-8")
        urls.append(f"/markets/{m['slug']}.html")
        print(f"  markets/{m['slug']}.html")

    (ROOT / "sitemap.xml").write_text(sitemap(urls), encoding="utf-8")
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n",
        encoding="utf-8",
    )
    print(f"\nSitemap: {len(urls)} URLs")


if __name__ == "__main__":
    print("Generating SEO pages...")
    main()
